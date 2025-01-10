from abc import ABC, abstractmethod

from git_rank.models.remote_repository import RemoteRepository


class AbstractGitRemoteRepository(ABC):

    @abstractmethod
    def get_repositories_by_user(self, username: str) -> list[RemoteRepository]:
        pass
