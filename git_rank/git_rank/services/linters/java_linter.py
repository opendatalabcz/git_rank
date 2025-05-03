import json
import math
import os
import subprocess
import tempfile

from git import Commit, PathLike
from structlog import get_logger

from git_rank.services.linters.abstract_linter import AbstractLinter

logger = get_logger()


class JavaLinter(AbstractLinter):

    def lint_commit_file(self, commit: Commit, file: PathLike) -> float:
        log = logger.bind(file=file)
        log.debug("lint_commit_file_java.start")

        # Use temporary file to isolate the commit file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".java", delete=False) as tmp_commit_file:
            tmp_commit_file.write(commit.tree[str(file)].data_stream.read().decode("utf8"))
            tmp_commit_file.flush()

            try:
                with open(tmp_commit_file.name, "r") as f:
                    lines = sum(1 for _ in f)

                    result = subprocess.run(
                        f"pmd check -d {tmp_commit_file.name}" + " " + self.arguments,
                        shell=True,
                        capture_output=True,
                        text=True,
                    )

                    if result.returncode != 0 and result.returncode != 4:
                        result.check_returncode()

                    result_json = json.loads(result.stdout)
                    result_files = result_json["files"]

                    if result_files:
                        violations = result_files[0]["violations"]
                        error_violations = len([v for v in violations if v["priority"] == 5])
                        other_violations = len(violations) - error_violations

                        lint_score = max(
                            0,
                            10.0 - ((float(5 * error_violations + other_violations) / lines) * 10),
                        )
                    else:
                        lint_score = 10

                log.debug(f"lint_commit_file_java.result.score: {lint_score}")
            except:
                log.exception("lint_commit_file_java.error")
                lint_score = 0
            finally:
                os.unlink(tmp_commit_file.name)

            log.debug("lint_commit_file_java.end")
            return lint_score
