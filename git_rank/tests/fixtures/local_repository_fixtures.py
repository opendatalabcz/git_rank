from unittest.mock import MagicMock

import pytest

from git_rank.models.local_repository import LocalRepository
from git_rank.models.user_data import UserData


@pytest.fixture(name="local_repository_fixture")
def local_repository_fixture(
    user_data_fixture: UserData,
    repo_fixture: MagicMock,
) -> LocalRepository:

    return LocalRepository(
        repository=repo_fixture,
        full_name="REPOSITORY_FULL_NAME",
        user=user_data_fixture,
    )
