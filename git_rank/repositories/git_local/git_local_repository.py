import os

from git import Repo, rmtree

from git_rank import STORAGE_DIR
from git_rank.models.local_repository import LocalRepository
from git_rank.models.remote_repository import RemoteRepository


class GitLocalRepository:
    def clone_repository(self, remote_repository: RemoteRepository) -> LocalRepository:
        repo = LocalRepository(
            repository=Repo.clone_from(
                url=remote_repository.clone_url,
                to_path=os.path.join(
                    STORAGE_DIR, remote_repository.username, remote_repository.full_name
                ),
            ),
            full_name=remote_repository.full_name,
            username=remote_repository.username,
        )

        return repo

    def delete_repository(self, local_repository: LocalRepository) -> None:
        rmtree(str(local_repository.repository.working_tree_dir))

    def delete_repositories_by_user(self, username: str) -> None:
        rmtree(os.path.join(STORAGE_DIR, username))
