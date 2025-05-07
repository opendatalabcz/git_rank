from dataclasses import dataclass

from git_rank.models.user_data import UserData


@dataclass
class RemoteRepository:
    clone_url: str
    full_name: str
    user: UserData
