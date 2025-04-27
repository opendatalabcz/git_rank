import os
import re
import tempfile
from io import StringIO

from git import Commit, PathLike
from pylint import epylint
from structlog import get_logger

from git_rank.services.linters.abstract_linter import AbstractLinter

logger = get_logger()

PYLINT_RANK_PATTERN = "[0-9]\.[0-9]+\/10"


class PythonLinter(AbstractLinter):

    def lint_commit_file(self, commit: Commit, file: PathLike) -> float:
        log = logger.bind(file=file)
        log.debug("lint_commit_file_python.start")

        # Use temporary file to isolate the commit file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp_commit_file:
            tmp_commit_file.write(commit.tree[str(file)].data_stream.read().decode("utf8"))
            tmp_commit_file.flush()

            try:
                lint_results: tuple[StringIO, StringIO] = epylint.py_run(
                    command_options=tmp_commit_file.name + " " + self.arguments, return_std=True
                )

                # Parse Pylint score (x/10) from the output
                lint_result = re.findall(PYLINT_RANK_PATTERN, lint_results[0].getvalue())
                if lint_result:
                    lint_score = float(str(lint_result[-1]).split("/")[0])
                    log.debug(
                        f"lint_commit_file_python.result.stdout: {lint_results[0].getvalue()}"
                    )
                else:
                    lint_score = 10

                log.debug(f"lint_commit_file_python.result.score: {lint_score}")
            except:
                log.exception("lint_commit_file_python.error")
            finally:
                os.unlink(tmp_commit_file.name)

            log.debug("lint_commit_file_python.end")
            return lint_score
