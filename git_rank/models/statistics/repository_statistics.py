from dataclasses import dataclass, field

from git_rank.models.statistics.commit_statistics import CommitStatistics
from git_rank.models.statistics.technology_statistics import TechnologyStatistics


@dataclass
class RepositoryStatistics:
    repository_name: str
    total_commits: int = 0
    user_commits: int = 0
    technologies: list[TechnologyStatistics] = field(default_factory=list)
    commits: list[CommitStatistics] = field(default_factory=list)
