from abc import ABC, abstractmethod

from git import Commit, PathLike


class AbstractLinter(ABC):
    # TODO create linting return type (score?, code smells? ...)
    @abstractmethod
    def lint_commit_file(self, commit: Commit, file: PathLike) -> None:
        pass
