from git import Repo
from structlog import get_logger

from git_rank.services.git.abstract_git_service import AbstractGitService

logger = get_logger()


class RepositoryCloner:
    def __init__(self, git_service: AbstractGitService):
        self.git_service = git_service

    def clone_repositories(self, username: str) -> list[Repo]:
        log = logger.bind(username=username)
        log.debug("clone_repositories.start")

        remote_repositories = self.git_service.get_repositories_by_user(username)
        local_repositories = []
        for remote_repository in remote_repositories:
            local_repositories.append(
                self.git_service.clone_repository(remote_repository)
            )

        log.debug("clone_repositories.end")
        return local_repositories
