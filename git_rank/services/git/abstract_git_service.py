import os
from abc import ABC, abstractmethod

from git import Repo as LocalRepository

from git_rank import STORAGE_DIR
from git_rank.models.remote_repository import RemoteRepository


class AbstractGitService(ABC):

    @abstractmethod
    def get_repositories_by_user(self, username: str) -> list[RemoteRepository]:
        pass

    def clone_repository(self, remote_repository: RemoteRepository) -> LocalRepository:
        repo = LocalRepository.clone_from(
            url=remote_repository.clone_url,
            to_path=os.path.join(STORAGE_DIR, remote_repository.full_name),
        )

        return repo

    def remove_repository(self) -> None:
        pass
