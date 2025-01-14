from structlog import get_logger

from git_rank.application.repository_cleaner import RepositoryCleaner
from git_rank.application.repository_cloner import RepositoryCloner
from git_rank.application.statistics_analyzer import StatisticsAnalyzer
from git_rank.models.local_repository import LocalRepository

logger = get_logger()


class RankingOrchestrator:
    def __init__(
        self,
        repository_cloner: RepositoryCloner,
        statistics_analyzer: StatisticsAnalyzer,
        repository_cleaner: RepositoryCleaner,
    ):
        self.repository_cloner = repository_cloner
        self.statistics_analyzer = statistics_analyzer
        self.repository_cleaner = repository_cleaner

    def rank_user(self, username: str) -> None:
        log = logger.bind(username=username)
        log.debug("rank_user.start")

        try:
            local_repositories: list[LocalRepository] = self.repository_cloner.clone_repositories(
                username
            )
            for local_repository in local_repositories:
                log.info(f"Ranking repository {local_repository.full_name}")

                repo_statistics = self.statistics_analyzer.analyze_basic_statistics(
                    local_repository
                )

                log.info(
                    repo=local_repository.full_name,
                    stats=repo_statistics,
                )
                # TODO other ranking
        except:
            log.exception("Error ranking user")

        self.repository_cleaner.remove_repositories_by_user(username)
        log.debug("rank_user.end")
