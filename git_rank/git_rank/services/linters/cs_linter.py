import os
import subprocess
import tempfile
from xml.etree import ElementTree

from git import Commit, PathLike
from structlog import get_logger

from git_rank.services.linters.abstract_linter import AbstractLinter

logger = get_logger()

OUTPUT_XML_FILE = "lint_result.xml"
TEMPORARY_COMMIT_FILE = "lint.cs"


class CSLinter(AbstractLinter):

    def lint_commit_file(self, commit: Commit, file: PathLike) -> float:
        log = logger.bind(file=file)
        log.debug("lint_commit_file_cs.start")

        # Use temporary file to isolate the commit file
        with (
            tempfile.TemporaryDirectory() as tmp_dir,
            open(os.path.join(tmp_dir, TEMPORARY_COMMIT_FILE), "w") as tmp_commit_file,
        ):
            tmp_commit_file.write(commit.tree[str(file)].data_stream.read().decode("utf8"))
            tmp_commit_file.flush()

            try:
                # Create temporary dotnet project (analysis cannot be done on single file)
                subprocess.run(
                    "dotnet new console",
                    shell=True,
                    capture_output=False,
                    cwd=tmp_dir,
                )
                with open(tmp_commit_file.name, "r") as f:
                    lines = sum(1 for _ in f)

                    subprocess.run(
                        f"roslynator analyze {self.arguments} -o {OUTPUT_XML_FILE}",
                        shell=True,
                        capture_output=False,
                        cwd=tmp_dir,
                    )

                if os.path.exists(os.path.join(tmp_dir, OUTPUT_XML_FILE)):
                    with open(os.path.join(tmp_dir, OUTPUT_XML_FILE), "r") as r:
                        result_xml_root = ElementTree.parse(r).getroot()

                        violations = result_xml_root.findall(
                            "./CodeAnalysis/Projects/Project/Diagnostics/Diagnostic"
                        )
                        error_violations = len(
                            [
                                v
                                for v in violations
                                if v.find("./Severity") is not None
                                and v.find("./Severity").text == "Error"  # type: ignore[union-attr] # None check is performed
                            ]
                        )
                        other_violations = len(violations) - error_violations

                        lint_score = max(
                            0,
                            10.0 - ((float(5 * error_violations + other_violations) / lines) * 10),
                        )
                else:
                    lint_score = 10

                log.debug(f"lint_commit_file_cs.result.score: {lint_score}")
            except:
                log.exception("lint_commit_file_cs.error")
            finally:
                os.unlink(tmp_commit_file.name)

            log.debug("lint_commit_file_cs.end")
            return lint_score
