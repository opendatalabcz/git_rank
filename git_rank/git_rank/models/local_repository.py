from dataclasses import dataclass

from git import Repo

from git_rank.git_rank.models.user_data import UserData


@dataclass
class LocalRepository:
    repository: Repo
    full_name: str
    user: UserData
