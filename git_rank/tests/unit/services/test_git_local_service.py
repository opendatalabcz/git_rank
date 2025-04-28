from typing import Iterator, cast

from unittest.mock import MagicMock, create_autospec

import pytest

from git_rank.models.local_repository import LocalRepository
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


def test_remove_repository(
    git_local_service_fixture: GitLocalService,
    git_local_repository_fixture: MagicMock,
    local_repository_fixture: LocalRepository,
) -> None:
    git_local_service_fixture.remove_repository(local_repository_fixture)

    git_local_repository_fixture.delete_repository.assert_called_once_with(local_repository_fixture)


def test_remove_user_repositories(
    git_local_service_fixture: GitLocalService,
    git_local_repository_fixture: MagicMock,
) -> None:
    USERNAME = "TEST_USERNAME"

    git_local_service_fixture.remove_user_repositories(USERNAME)

    git_local_repository_fixture.delete_repositories_by_user.assert_called_once_with(USERNAME)


def test_filter_user_commits(
    git_local_service_fixture: GitLocalService,
    local_repository_fixture: LocalRepository,
    repo_fixture: MagicMock,
) -> None:

    user_commits = git_local_service_fixture.filter_user_commits(local_repository_fixture)

    repo_fixture.iter_commits.assert_called_once()

    for user_commit in user_commits:
        assert (
            user_commit.author.name == local_repository_fixture.user.user_name
            or user_commit.author.name == local_repository_fixture.user.username
            or user_commit.author.email == local_repository_fixture.user.user_email
        )
