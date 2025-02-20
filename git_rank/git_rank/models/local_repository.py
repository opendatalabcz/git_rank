from dataclasses import dataclass

from git import Repo


@dataclass
class LocalRepository:
    repository: Repo
    full_name: str
    username: str
