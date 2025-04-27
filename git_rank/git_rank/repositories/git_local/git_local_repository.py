import os

from git import Repo, rmtree

from git_rank import STORAGE_DIR
from git_rank.models.local_repository import LocalRepository
from git_rank.models.remote_repository import RemoteRepository


class GitLocalRepository:
    """Class to manage (clone, delete) local git repositories."""

    def clone_repository(self, remote_repository: RemoteRepository) -> LocalRepository:
        """Clone a remote repository to a local directory.
        Args:
            remote_repository (RemoteRepository): The remote repository to clone.
        Returns:
            LocalRepository: The cloned local repository.
        """
        repo = LocalRepository(
            repository=Repo.clone_from(
                url=remote_repository.clone_url,
                to_path=os.path.join(
                    STORAGE_DIR, remote_repository.user.username, remote_repository.full_name
                ),
            ),
            full_name=remote_repository.full_name,
            user=remote_repository.user,
        )

        return repo

    def delete_repository(self, local_repository: LocalRepository) -> None:
        """Delete a local repository.
        Args:
            local_repository (LocalRepository): The local repository to delete.
        """
        if os.path.exists(str(local_repository.repository.working_tree_dir)):
            rmtree(str(local_repository.repository.working_tree_dir))

    def delete_repositories_by_user(self, username: str) -> None:
        """Delete all local repositories for a given user.
        Args:
            username (str): The username of the user whose repositories to delete.
        """
        if os.path.exists(os.path.join(STORAGE_DIR, username)):
            rmtree(os.path.join(STORAGE_DIR, username))
