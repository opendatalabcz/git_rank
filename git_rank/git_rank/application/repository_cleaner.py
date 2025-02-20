from structlog import get_logger

from git_rank.models.local_repository import LocalRepository
from git_rank.services.git_local_service import GitLocalService

logger = get_logger()


class RepositoryCleaner:
    def __init__(self, git_local_service: GitLocalService):
        self.git_local_service = git_local_service

    def remove_repositories(self, local_repositories: list[LocalRepository]) -> None:
        logger.debug(
            "remove_repositories.start",
            local_repositores=map(lambda repo: repo.full_name, local_repositories),
        )

        for local_repository in local_repositories:
            logger.info(f"Removing repository {local_repository.full_name}")
            self.git_local_service.remove_repository(local_repository)

        logger.debug("remove_repositories.end")

    def remove_repositories_by_user(self, username: str) -> None:
        log = logger.bind(username=username)
        log.debug("remove_repositories_by_user.start")

        self.git_local_service.remove_user_repositories(username)

        log.debug("remove_repositories_by_user.end")
