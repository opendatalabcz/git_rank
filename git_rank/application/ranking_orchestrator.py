from structlog import get_logger

from git_rank.application.repository_cloner import RepositoryCloner

logger = get_logger()


class RankingOrchestrator:
    def __init__(self, repository_cloner: RepositoryCloner):
        self.repository_cloner = repository_cloner

    def rank_user(self, username: str) -> None:
        log = logger.bind(username=username)
        log.debug("rank_user.start")

        self.repository_cloner.clone_repositories(username)

        log.debug("rank_user.end")
