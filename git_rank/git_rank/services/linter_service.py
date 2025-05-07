from git import Commit, PathLike

from git_rank.models.statistics.technology_statistics import TechnologyType
from git_rank.services.linters.cs_linter import CSLinter
from git_rank.services.linters.java_linter import JavaLinter
from git_rank.services.linters.python_linter import PythonLinter


class LinterService:
    """
    Service to manage all available linters.
    The service is responsible for running linters on files in a commit.
    """

    def __init__(self, python_linter: PythonLinter, java_linter: JavaLinter, cs_linter: CSLinter):
        self.python_linter = python_linter
        self.java_linter = java_linter
        self.cs_linter = cs_linter

    def lint_commit_file(self, commit: Commit, file: PathLike, technology: TechnologyType) -> float:
        """
        Lint a file in a commit.
        Args:
            commit (Commit): The Commit object to lint the file from.
            file (PathLike): The file to lint.
            technology (TechnologyType): The technology type of the file.
        Returns:
            float: The lint score of the file (0-10).
        """
        lint_score: float = 0

        match technology:
            case TechnologyType.PYTHON:
                lint_score = self.python_linter.lint_commit_file(commit, file)
            case TechnologyType.JAVA:
                lint_score = self.java_linter.lint_commit_file(commit, file)
            case TechnologyType.CS:
                lint_score = self.cs_linter.lint_commit_file(commit, file)

        return lint_score
