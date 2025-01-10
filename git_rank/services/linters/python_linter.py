import os

from git import Commit, PathLike
from pylint import lint
from structlog import get_logger

from git_rank.services.linters.abstract_linter import AbstractLinter

logger = get_logger()


class PythonLinter(AbstractLinter):

    def lint_commit_file(self, commit: Commit, file: PathLike) -> None:
        logger.debug("Linting Python file", file=file)
        # TODO actual Python linting logic
