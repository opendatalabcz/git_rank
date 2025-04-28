from typing import Iterator, cast

from unittest.mock import MagicMock, create_autospec

import pytest

from git_rank.repositories.git_remote.abstract_git_remote_repository import (
    AbstractGitRemoteRepository,
)
from git_rank.services.git_remote_service import GitRemoteService
from tests.fixtures.user_data_fixtures import TEST_USERNAME


@pytest.fixture(name="git_remote_repository_fixture")
def git_remote_repository_fixture() -> MagicMock:
    git_remote_repository = cast(
        MagicMock, create_autospec(AbstractGitRemoteRepository, instance=True)
    )

    return git_remote_repository


@pytest.fixture(name="git_remote_service_fixture")
def git_remote_service_fixture(
    git_remote_repository_fixture: MagicMock,
) -> Iterator[GitRemoteService]:
    yield GitRemoteService(git_remote_repository=git_remote_repository_fixture)


def test_get_user_repositories(
    git_remote_service_fixture: GitRemoteService,
    git_remote_repository_fixture: MagicMock,
) -> None:

    git_remote_service_fixture.get_user_repositories(TEST_USERNAME)

    git_remote_repository_fixture.get_repositories_by_user.assert_called_once_with(TEST_USERNAME)
