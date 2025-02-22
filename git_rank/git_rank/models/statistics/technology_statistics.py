from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TechnologyType(Enum):
    PYTHON = "PYTHON"
    JAVA = "JAVA"
    OTHER = "OTHER"


@dataclass
class TechnologyStatistics:
    technology: TechnologyType
    total_changes: int
    first_used: datetime
    last_used: datetime

    @staticmethod
    def map_file_extension_to_technology(file_extension: str) -> TechnologyType:
        extension_mapping = {
            ".py": TechnologyType.PYTHON,
            ".java": TechnologyType.JAVA,
        }

        return extension_mapping.get(file_extension, TechnologyType.OTHER)
