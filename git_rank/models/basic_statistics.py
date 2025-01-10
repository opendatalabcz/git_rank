from dataclasses import dataclass


@dataclass
class BasicStatistics:
    total_commits: int | None = None
    user_commits: int | None = None
