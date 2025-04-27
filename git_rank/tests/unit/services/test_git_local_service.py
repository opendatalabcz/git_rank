from typing import Iterator, cast

from unittest.mock import MagicMock, create_autospec

import pytest

from git_rank.models.remote_repository import RemoteRepository
from git_rank.repositories.git_local.git_local_repository import GitLocalRepository
from git_rank.services.git_local_service import GitLocalService


@pytest.fixture(name="git_local_repository_fixture")
def git_local_repository_fixture() -> MagicMock:
    git_local_repository = cast(MagicMock, create_autospec(GitLocalRepository, instance=True))
    return git_local_repository


@pytest.fixture(name="git_local_service_fixture")
def git_local_service_fixture(
    git_local_repository_fixture: MagicMock,
) -> Iterator[GitLocalService]:
    yield GitLocalService(git_local_repository=git_local_repository_fixture)


def test_clone_repository(
    git_local_service_fixture: GitLocalService,
    git_local_repository_fixture: MagicMock,
    remote_repository_fixture: RemoteRepository,
) -> None:
    git_local_service_fixture.clone_repository(remote_repository_fixture)

    git_local_repository_fixture.clone_repository.assert_called_once_with(remote_repository_fixture)
