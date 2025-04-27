from abc import ABC, abstractmethod

from git_rank.models.remote_repository import RemoteRepository


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

    @abstractmethod
    def get_user_repository_by_url(self, username: str, repository_url: str) -> RemoteRepository:
        """
        Get a specific repository for a given user by URL.
        Args:
            username (str): The username of the user.
            repository_url (str): The URL of the repository.
        Returns:
            A RemoteRepository object representing the found git repository and users metadata.
        """
        pass
