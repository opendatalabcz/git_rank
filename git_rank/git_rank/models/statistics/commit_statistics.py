from dataclasses import dataclass, field

from git_rank.models.statistics.file_statistics import FileStatistics


@dataclass
class CommitStatistics:
    average_lint_score: float = 0
    files: list[FileStatistics] = field(default_factory=list)
