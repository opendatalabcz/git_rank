from typing import Iterator, cast

from unittest.mock import MagicMock, create_autospec

import pytest

from git_rank.application.repository_cloner import RepositoryCloner
from git_rank.models.local_repository import LocalRepository
from git_rank.models.remote_repository import RemoteRepository
from git_rank.services.git_local_service import GitLocalService
from git_rank.services.git_remote_service import GitRemoteService

TEST_USERNAME = "test-user"
TEST_REPOSITORY_URL = f"https://www.example.com/{TEST_USERNAME}/test-repo.git"


@pytest.fixture(name="git_remote_service_fixture")
def git_remote_service_fixture(remote_repository_fixture: RemoteRepository) -> MagicMock:
    git_remote_service = cast(MagicMock, create_autospec(GitRemoteService, instance=True))
    git_remote_service.get_user_repositories.return_value = [remote_repository_fixture]
    git_remote_service.get_user_repository_by_url.return_value = remote_repository_fixture

    return git_remote_service


@pytest.fixture(name="git_local_service_fixture")
def git_local_service_fixture(local_repository_fixture: LocalRepository) -> MagicMock:
    git_local_service = cast(MagicMock, create_autospec(GitLocalService, instance=True))
    git_local_service.clone_repository.return_value = local_repository_fixture

    return git_local_service


@pytest.fixture(name="repository_cloner_fixture")
def repository_cloner_fixture(
    git_remote_service_fixture: MagicMock, git_local_service_fixture: MagicMock
) -> Iterator[RepositoryCloner]:
    yield RepositoryCloner(
        git_remote_service=git_remote_service_fixture, git_local_service=git_local_service_fixture
    )


def test_clone_repositories(
    git_remote_service_fixture: MagicMock,
    git_local_service_fixture: MagicMock,
    remote_repository_fixture: RemoteRepository,
    local_repository_fixture: LocalRepository,
    repository_cloner_fixture: RepositoryCloner,
) -> None:

    cloned_repositories = repository_cloner_fixture.clone_repositories(username=TEST_USERNAME)

    git_remote_service_fixture.get_user_repositories.assert_called_once_with(TEST_USERNAME)
    git_local_service_fixture.clone_repository.assert_called_once_with(remote_repository_fixture)

    assert cloned_repositories == [local_repository_fixture]


def test_clone_user_repository(
    git_remote_service_fixture: MagicMock,
    git_local_service_fixture: MagicMock,
    remote_repository_fixture: RemoteRepository,
    local_repository_fixture: LocalRepository,
    repository_cloner_fixture: RepositoryCloner,
) -> None:

    cloned_repository = repository_cloner_fixture.clone_user_repository(
        username=TEST_USERNAME, repository_url=TEST_REPOSITORY_URL
    )

    git_remote_service_fixture.get_user_repository_by_url.assert_called_once_with(
        username=TEST_USERNAME, repository_url=TEST_REPOSITORY_URL
    )
    git_local_service_fixture.clone_repository.assert_called_once_with(remote_repository_fixture)

    assert cloned_repository == local_repository_fixture
