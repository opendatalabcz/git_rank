from dataclasses import dataclass
from enum import Enum

from git_rank.models.statistics.technology_statistics import TechnologyType


class FileState(Enum):
    ADDED = "ADDED"
    CHANGED = "CHANGED"


@dataclass
class FileStatistics:
    file_name: str
    lint_score: float
    file_state: FileState
    technology: TechnologyType
