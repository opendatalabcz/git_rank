from typing import Counter

import os

from git import Commit, PathLike
from structlog import get_logger

from git_rank.models.basic_statistics import BasicStatistics, TechnologyStatistics, TechnologyType
from git_rank.models.local_repository import LocalRepository
from git_rank.services.git_local_service import GitLocalService
from git_rank.services.linter_service import LinterService

logger = get_logger()


class StatisticsAnalyzer:
    def __init__(self, git_local_service: GitLocalService, linter_service: LinterService):
        self.git_local_service = git_local_service
        self.linter_service = linter_service

    def analyze_basic_statistics(self, local_repository: LocalRepository) -> BasicStatistics:
        log = logger.bind(repository=local_repository.full_name)
        log.debug("analyze_basic_statistics.start")

        basic_statistics: BasicStatistics = BasicStatistics()

        user_commits = self.git_local_service.filter_user_commits(local_repository)
        basic_statistics.total_commits = len(list(local_repository.repository.iter_commits()))
        basic_statistics.user_commits = len(user_commits)

        basic_statistics.technologies = self._analyze_technologies(user_commits)

        log.debug("analyze_basic_statistics.end")
        return basic_statistics

    def _analyze_technologies(self, commits: list[Commit]) -> list[TechnologyStatistics]:
        file_types: Counter[TechnologyType] = Counter()
        technology_statistics: list[TechnologyStatistics] = []

        for commit in commits:
            changed_files = list(commit.stats.files.keys())
            for file in changed_files:
                technology = TechnologyStatistics.map_file_extension_to_technology(
                    os.path.splitext(file)[1]
                )
                file_types.update([technology])
                if technology != TechnologyType.OTHER:
                    self._lint_file(commit, file, technology)

        for file_type in file_types.items():
            technology_statistics.append(
                TechnologyStatistics(
                    technology=file_type[0],
                    changes=file_type[1],
                )
            )

        return technology_statistics

    def _lint_file(self, commit: Commit, file: PathLike, technology: TechnologyType) -> None:
        self.linter_service.lint_commit_file(commit, file, technology)
