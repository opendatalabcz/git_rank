from git import Commit, PathLike

from git_rank.models.statistics.technology_statistics import TechnologyType
from git_rank.services.linters.java_linter import JavaLinter
from git_rank.services.linters.python_linter import PythonLinter


class LinterService:
    def __init__(self, python_linter: PythonLinter, java_linter: JavaLinter):
        self.python_linter = python_linter
        self.java_linter = java_linter

    def lint_commit_file(self, commit: Commit, file: PathLike, technology: TechnologyType) -> float:
        lint_score: float = 0

        match technology:
            case TechnologyType.PYTHON:
                lint_score = self.python_linter.lint_commit_file(commit, file)
            case TechnologyType.JAVA:
                lint_score = self.java_linter.lint_commit_file(commit, file)

        return lint_score
