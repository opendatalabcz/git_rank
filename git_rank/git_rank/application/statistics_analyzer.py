import os
from collections import defaultdict
from datetime import datetime

from git import Commit, PathLike
from structlog import get_logger

from git_rank.constants.git_rank_constants import GitRankConstants
from git_rank.models.local_repository import LocalRepository
from git_rank.models.statistics.commit_statistics import CommitStatistics
from git_rank.models.statistics.file_statistics import FileState, FileStatistics
from git_rank.models.statistics.repository_statistics import RepositoryStatistics
from git_rank.models.statistics.technology_statistics import TechnologyStatistics, TechnologyType
from git_rank.services.git_local_service import GitLocalService
from git_rank.services.linter_service import LinterService

logger = get_logger()


class StatisticsAnalyzer:
    """
    Class responsible for analyzing the statistics of a local repository.
    """

    def __init__(self, git_local_service: GitLocalService, linter_service: LinterService):
        self.git_local_service = git_local_service
        self.linter_service = linter_service

    def analyze_repository_statistics(
        self, local_repository: LocalRepository
    ) -> RepositoryStatistics:
        log = logger.bind(repository=local_repository.full_name)
        log.debug("analyze_repository_statistics.start")

        repository_statistics: RepositoryStatistics = RepositoryStatistics(
            repository_name=local_repository.full_name
        )

        user_commits = self.git_local_service.filter_user_commits(local_repository)

        repository_statistics.total_commits = len(list(local_repository.repository.iter_commits()))
        repository_statistics.user_commits = len(user_commits)
        repository_statistics.commits = self._analyze_commits(user_commits)
        repository_statistics.technologies = self._analyze_technologies(
            repository_statistics.commits
        )

        log.debug("analyze_repository_statistics.end")
        return repository_statistics

    def analyze_cross_repository_statistics(
        self, user_repositories_statistics: list[RepositoryStatistics]
    ) -> RepositoryStatistics | None:
        """
        Aggregates the cross-repository statistics from list of previously computed statistics of given repositories.
        """
        logger.debug("analyze_cross_repository_statistics.start")

        if len(user_repositories_statistics) == 1:
            return None

        cross_repository_statistics: RepositoryStatistics = RepositoryStatistics(
            repository_name=GitRankConstants.CROSS_REPOSITORY_NAME
        )

        cross_repository_statistics.total_commits = sum(
            user_repository_statistics.total_commits
            for user_repository_statistics in user_repositories_statistics
        )
        cross_repository_statistics.user_commits = sum(
            user_repository_statistics.user_commits
            for user_repository_statistics in user_repositories_statistics
        )
        cross_repository_statistics.commits = sum(
            [
                user_repository_statistics.commits
                for user_repository_statistics in user_repositories_statistics
            ],
            [],
        )
        cross_repository_statistics.technologies = self._analyze_technologies(
            cross_repository_statistics.commits
        )

        return cross_repository_statistics

    def _analyze_commits(self, commits: list[Commit]) -> list[CommitStatistics]:
        commits_statistics: list[CommitStatistics] = []

        for commit in commits:
            commits_statistics.append(self._analyze_commit(commit))

        return commits_statistics

    def _analyze_commit(self, commit: Commit) -> CommitStatistics:
        """
        Analyzes a single commit and returns the commit statistics.
        """
        commit_statistics = CommitStatistics(
            commit_sha=commit.hexsha, commit_date=datetime.fromtimestamp(commit.committed_date)
        )

        commit_files = commit.stats.files

        if commit_files:
            for commit_file in commit_files.items():
                if commit_file[1]["change_type"] != "M" and commit_file[1]["change_type"] != "A":
                    continue

                technology = TechnologyStatistics.map_file_extension_to_technology(
                    os.path.splitext(commit_file[0])[1]
                )

                lint_score = self._lint_file(commit, commit_file[0], technology)

                # If modified calculate the difference in lint score from the parent commit
                if commit_file[1]["change_type"] == "M":
                    lint_score_before = self._lint_file(
                        commit.parents[0], commit_file[0], technology
                    )
                    lint_score = lint_score - lint_score_before
                    file_state = FileState.CHANGED
                else:
                    file_state = FileState.ADDED

                commit_statistics.files.append(
                    FileStatistics(
                        file_name=str(commit_file[0]),
                        lint_score=lint_score,
                        file_state=file_state,
                        technology=technology,
                    ),
                )
            commit_statistics.average_add_lint_score = self._calculate_average_lint_score(
                commit_statistics.files, FileState.ADDED
            )
            commit_statistics.average_change_lint_score = self._calculate_average_lint_score(
                commit_statistics.files, FileState.CHANGED
            )

        return commit_statistics

    def _analyze_technologies(
        self, commit_statistics: list[CommitStatistics]
    ) -> list[TechnologyStatistics]:
        """
        Analyzes the technologies used in previously analyzed commits and returns the technology statistics.
        """
        technology_statistics: dict[TechnologyType, TechnologyStatistics] = {}
        technology_weeks = defaultdict(set)

        for commit in commit_statistics:
            for file in commit.files:
                technology_weeks[file.technology].add(commit.commit_date.isocalendar()[:2])
                technology_statistic = technology_statistics.get(file.technology)
                if technology_statistic:
                    technology_statistics[file.technology] = TechnologyStatistics(
                        technology=file.technology,
                        total_changes=technology_statistic.total_changes + 1,
                        first_used_date=min(
                            technology_statistic.first_used_date, commit.commit_date
                        ),
                        last_used_date=max(technology_statistic.last_used_date, commit.commit_date),
                        weeks_used=len(technology_weeks[file.technology]),
                    )
                else:
                    technology_statistics[file.technology] = TechnologyStatistics(
                        technology=file.technology,
                        total_changes=1,
                        first_used_date=commit.commit_date,
                        last_used_date=commit.commit_date,
                        weeks_used=len(technology_weeks[file.technology]),
                    )

        return list(technology_statistics.values())

    def _lint_file(self, commit: Commit, file: PathLike, technology: TechnologyType) -> float:
        return self.linter_service.lint_commit_file(commit, file, technology)

    def _calculate_average_lint_score(
        self, files: list[FileStatistics], file_state: FileState
    ) -> float | None:
        total = len(
            list(
                filter(
                    lambda file: file.file_state == file_state
                    and file.technology != TechnologyType.OTHER,
                    files,
                )
            )
        )

        return (
            sum(
                file.lint_score
                for file in files
                if file.file_state == file_state and file.technology != TechnologyType.OTHER
            )
            / total
            if total
            else None
        )
