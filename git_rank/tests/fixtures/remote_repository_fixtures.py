import pytest

from git_rank.models.remote_repository import RemoteRepository
from git_rank.models.user_data import UserData


@pytest.fixture(name="remote_repository_fixture")
def remote_repository_fixture(
    user_data_fixture: UserData,
) -> RemoteRepository:
    return RemoteRepository(
        clone_url="REPOSITORY_CLONE_URL",
        full_name="REPOSITORY_FULL_NAME",
        user=user_data_fixture,
    )
