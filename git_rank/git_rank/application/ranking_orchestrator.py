from structlog import get_logger

from git_rank.application.repository_cleaner import RepositoryCleaner
from git_rank.application.repository_cloner import RepositoryCloner
from git_rank.application.statistics_analyzer import StatisticsAnalyzer
from git_rank.models.local_repository import LocalRepository
from git_rank.models.statistics.repository_statistics import RepositoryStatistics
from git_rank.models.statistics.user_statistics import UserStatistics

logger = get_logger()


class RankingOrchestrator:
    """
    The orchestrator is responsible for coordinating the ranking process.
    Args:
        repository_cloner (RepositoryCloner): Class responsible for cloning repositories.
        statistics_analyzer (StatisticsAnalyzer): Class responsible for analyzing repositories.
        repository_cleaner (RepositoryCleaner): Class responsible for removing repositories.
    """

    def __init__(
        self,
        repository_cloner: RepositoryCloner,
        statistics_analyzer: StatisticsAnalyzer,
        repository_cleaner: RepositoryCleaner,
    ):
        self.repository_cloner = repository_cloner
        self.statistics_analyzer = statistics_analyzer
        self.repository_cleaner = repository_cleaner

    def rank_user(self, username: str) -> UserStatistics:
        """
        Rank a user by analyzing their repositories.
        Args:
            username (str): The username of the user to rank.
        Returns:
            UserStatistics: The statistics of the user and their repositories.
        """
        log = logger.bind(username=username)
        log.info("rank_user.start")

        repositories_statistics: list[RepositoryStatistics] = []
        cross_repositories_statistics: RepositoryStatistics | None = None

        local_repositories: list[LocalRepository] = self.repository_cloner.clone_repositories(
            username
        )

        try:
            for local_repository in local_repositories:
                log.info("rank_user.rank_repository.start", repository=local_repository.full_name)

                repositories_statistics.append(
                    self.statistics_analyzer.analyze_repository_statistics(local_repository)
                )

                log.info("rank_user.rank_repository.end", repository=local_repository.full_name)
            cross_repositories_statistics = (
                self.statistics_analyzer.analyze_cross_repository_statistics(
                    repositories_statistics
                )
            )
        except:
            log.exception("rank_user.error")
            raise Exception("Error while ranking user")
        finally:
            self.repository_cleaner.remove_repositories_by_user(username)

        log.info("rank_user.end")
        return UserStatistics(
            username=username,
            repositories=repositories_statistics,
            cross_repository=cross_repositories_statistics,
        )

    def rank_user_repository(self, username: str, repository_url: str) -> UserStatistics:
        """
        Rank a user by analyzing a specific repository.
        Args:
            username (str): The username of the user to rank.
            repository_url (str): The URL of the repository to analyze.
        Returns:
            UserStatistics: The statistics of the user and their repository.
        """
        log = logger.bind(username=username, repository_url=repository_url)
        log.info("rank_repository.start")

        repositories_statistics: list[RepositoryStatistics] = []

        try:
            local_repository: LocalRepository = self.repository_cloner.clone_user_repository(
                username=username, repository_url=repository_url
            )
            repositories_statistics.append(
                self.statistics_analyzer.analyze_repository_statistics(local_repository)
            )
        except:
            log.exception("rank_repository.error")

        self.repository_cleaner.remove_repositories_by_user(username)

        log.info("rank_repository.end")
        return UserStatistics(
            username=username, repositories=repositories_statistics, cross_repository=None
        )
