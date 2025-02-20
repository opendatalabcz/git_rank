from dataclasses import dataclass
from enum import Enum


class TechnologyType(Enum):
    PYTHON = "PYTHON"
    JAVA = "JAVA"
    OTHER = "OTHER"


@dataclass
class TechnologyStatistics:
    technology: TechnologyType
    total_changes: int

    @staticmethod
    def map_file_extension_to_technology(file_extension: str) -> TechnologyType:
        extension_mapping = {
            ".py": TechnologyType.PYTHON,
            ".java": TechnologyType.JAVA,
        }

        return extension_mapping.get(file_extension, TechnologyType.OTHER)
