from dataclasses import dataclass


@dataclass
class UserData:
    username: str
    user_name: str
    user_email: str | None = None
