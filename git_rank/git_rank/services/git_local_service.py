from git import Commit
from structlog import get_logger

from git_rank.models.local_repository import LocalRepository
from git_rank.models.remote_repository import RemoteRepository
from git_rank.repositories.git_local.git_local_repository import GitLocalRepository

logger = get_logger()


class GitLocalService:
    """Service to manage local repositories."""

    def __init__(self, git_local_repository: GitLocalRepository):
        self.git_local_repository = git_local_repository

    def clone_repository(self, remote_repository: RemoteRepository) -> LocalRepository:
        return self.git_local_repository.clone_repository(remote_repository)

    def remove_repository(self, local_repository: LocalRepository) -> None:
        self.git_local_repository.delete_repository(local_repository)

    def remove_user_repositories(self, username: str) -> None:
        self.git_local_repository.delete_repositories_by_user(username)

    def filter_user_commits(self, local_repository: LocalRepository) -> list[Commit]:
        log = logger.bind(repository=local_repository.full_name)
        log.debug("filter_user_commits.start")

        user_commits: list[Commit] = []
        for commit in local_repository.repository.iter_commits():
            # Compare with both name and email to account for different configurations
            if (
                commit.author.name == local_repository.user.user_name
                or commit.author.name == local_repository.user.username
                or commit.author.email == local_repository.user.user_email
            ):
                user_commits.append(commit)

        log.debug("filter_user_commits.end")
        return user_commits
