from dataclasses import dataclass, field
from datetime import datetime

from git_rank.models.statistics.file_statistics import FileStatistics


@dataclass
class CommitStatistics:
    commit_sha: str
    commit_date: datetime
    average_add_lint_score: float | None = None
    average_change_lint_score: float | None = None
    files: list[FileStatistics] = field(default_factory=list)
