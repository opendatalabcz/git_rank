from git_rank.models.local_repository import LocalRepository
from git_rank.models.remote_repository import RemoteRepository
from git_rank.repositories.git_remote.abstract_git_remote_repository import (
    AbstractGitRemoteRepository,
)


class GitRemoteService:
    def __init__(self, git_remote_repository: AbstractGitRemoteRepository):
        self.git_remote_repository = git_remote_repository

    def get_user_repositories(self, username: str) -> list[RemoteRepository]:
        return self.git_remote_repository.get_repositories_by_user(username)

    def get_user_repository_by_url(self, username: str, repository_url: str) -> RemoteRepository:
        return self.git_remote_repository.get_user_repository_by_url(username, repository_url)
