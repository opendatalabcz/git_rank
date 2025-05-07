from typing import TypedDict

from abc import ABC, abstractmethod

from git import Commit, PathLike


class LinterConfig(TypedDict):
    arguments: str


class AbstractLinter(ABC):

    def __init__(self, linter_config: LinterConfig) -> None:
        self.arguments = linter_config["arguments"]

    @abstractmethod
    def lint_commit_file(self, commit: Commit, file: PathLike) -> float:
        pass
