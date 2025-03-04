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

        with tempfile.NamedTemporaryFile(mode="w", suffix=".java", delete=False) as tmp_commit_file:
            tmp_commit_file.write(commit.tree[str(file)].data_stream.read().decode("utf8"))
            tmp_commit_file.flush()

            try:
                with open(tmp_commit_file.name, "r") as f:
                    lines = sum(1 for _ in f)

                if lines:
                    result = subprocess.run(
                        f"pmd check -d {tmp_commit_file.name}" + " " + self.arguments,
                        shell=True,
                        capture_output=True,
                        text=True,
                    )

                    errors = len(result.stdout.split("\n")) - 1
                    error_rate = errors / lines
                    lint_score = max(1, 10 * math.exp(-error_rate * 5))
                else:
                    lint_score = 10

                log.debug(f"lint_commit_file_java.result.score: {lint_score}")
            except:
                log.exception("lint_commit_file_java.error")
            finally:
                os.unlink(tmp_commit_file.name)

            log.debug("lint_commit_file_java.end")
            return lint_score
