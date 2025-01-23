from dataclasses import dataclass
from enum import Enum


class FileState(Enum):
    ADDED = "ADDED"
    CHANGED = "CHANGED"


@dataclass
class FileStatistics:
    file_name: str
    lint_score: str
    file_state: FileState
