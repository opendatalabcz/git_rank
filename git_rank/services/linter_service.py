import os

from git import Commit, PathLike

from git_rank.models.statistics.technology_statistics import TechnologyStatistics, TechnologyType
from git_rank.services.linters.python_linter import PythonLinter


class LinterService:
    def __init__(self, python_linter: PythonLinter):
        self.python_linter = python_linter

    def lint_commit_file(self, commit: Commit, file: PathLike) -> str:
        technology = TechnologyStatistics.map_file_extension_to_technology(
            os.path.splitext(file)[1]
        )
        lint_score: str = "0"

        match technology:
            case TechnologyType.PYTHON:
                lint_score = self.python_linter.lint_commit_file(commit, file)
            # TODO other linters

        return lint_score
