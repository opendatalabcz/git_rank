from dataclasses import dataclass


@dataclass
class RemoteRepository:
    clone_url: str
    full_name: str
    username: str
    user_name: str
    user_email: str
