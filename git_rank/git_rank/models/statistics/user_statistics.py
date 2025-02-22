from dataclasses import dataclass

from git_rank.git_rank.models.statistics.repository_statistics import RepositoryStatistics


@dataclass
class UserStatistics:
    username: str
    repositories: list[RepositoryStatistics]
