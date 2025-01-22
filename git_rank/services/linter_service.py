from git import Commit, PathLike

from git_rank.models.repository_statistics import TechnologyType
from git_rank.services.linters.python_linter import PythonLinter


class LinterService:
    def __init__(self, python_linter: PythonLinter):
        self.python_linter = python_linter

    def lint_commit_file(self, commit: Commit, file: PathLike, technology: TechnologyType) -> None:
        match technology:
            case TechnologyType.PYTHON:
                self.python_linter.lint_commit_file(commit, file)
            # TODO other linters
