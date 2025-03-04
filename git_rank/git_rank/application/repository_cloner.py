from structlog import get_logger

from git_rank.models.local_repository import LocalRepository
from git_rank.services.git_local_service import GitLocalService
from git_rank.services.git_remote_service import GitRemoteService

logger = get_logger()


class RepositoryCloner:
    def __init__(self, git_remote_service: GitRemoteService, git_local_service: GitLocalService):
        self.git_remote_service = git_remote_service
        self.git_local_service = git_local_service

    def clone_repositories(self, username: str) -> list[LocalRepository]:
        log = logger.bind(username=username)
        log.debug("clone_repositories.start")

        remote_repositories = self.git_remote_service.get_user_repositories(username)
        local_repositories = []
        for remote_repository in remote_repositories:
            local_repositories.append(self.git_local_service.clone_repository(remote_repository))

        log.debug("clone_repositories.end")
        return local_repositories

    def clone_user_repository(self, username: str, repository_url: str) -> LocalRepository:
        log = logger.bind(username=username, repository_url=repository_url)
        log.debug("clone_user_repository.start")

        remote_repository = self.git_remote_service.get_user_repository_by_url(
            username, repository_url
        )
        local_repository = self.git_local_service.clone_repository(remote_repository)

        log.debug("clone_user_repository.end")
        return local_repository
