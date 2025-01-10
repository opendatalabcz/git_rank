from structlog import get_logger

from git_rank.models.basic_statistics import BasicStatistics
from git_rank.models.local_repository import LocalRepository
from git_rank.services.git_local_service import GitLocalService

logger = get_logger()


class StatisticsAnalyzer:
    def __init__(self, git_local_service: GitLocalService):
        self.git_local_service = git_local_service

    def analyze_basic_statistics(
        self, local_repository: LocalRepository
    ) -> BasicStatistics:
        log = logger.bind(repository=local_repository.full_name)
        log.debug("analyze_basic_statistics.start")

        basic_statistics: BasicStatistics = BasicStatistics()

        user_commits = self.git_local_service.filter_user_commits(local_repository)
        basic_statistics.total_commits = len(
            list(local_repository.repository.iter_commits())
        )
        basic_statistics.user_commits = len(user_commits)

        log.debug("analyze_basic_statistics.end")
        return basic_statistics
