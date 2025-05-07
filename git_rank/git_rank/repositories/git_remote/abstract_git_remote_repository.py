from abc import ABC, abstractmethod

from git_rank.models.remote_repository import RemoteRepository
from git_rank.models.user_data import UserData


class AbstractGitRemoteRepository(ABC):
    """
    Abstract class for Git remote repository.
    This class defines the interface for interacting with remote Git repositories.
    """

    @abstractmethod
    def get_repositories_by_user(self, username: str) -> list[RemoteRepository]:
        """
        Get all repositories for a given user.
        Args:
            username (str): The username of the user.
        Returns:
            A list of RemoteRepository objects representing all found git repositories.
        """
        pass

    def get_user_repository_by_url(self, username: str, repository_url: str) -> RemoteRepository:
        return RemoteRepository(
            clone_url=repository_url,
            full_name=repository_url.split("/")[-1].split(".git")[0],
            user=UserData(username=username, user_name=username, user_email=None),
        )
