from typing import Iterator, cast

from unittest.mock import MagicMock, create_autospec

import pytest

from git_rank.application.repository_cleaner import RepositoryCleaner
from git_rank.models.local_repository import LocalRepository
from git_rank.services.git_local_service import GitLocalService

TEST_USERNAME = "test-user"


@pytest.fixture(name="git_local_service_fixture")
def git_local_service_fixture() -> MagicMock:
    git_local_service = cast(MagicMock, create_autospec(GitLocalService, instance=True))

    return git_local_service


@pytest.fixture(name="repository_cleaner_fixture")
def repository_cleaner_fixture(git_local_service_fixture: MagicMock) -> Iterator[RepositoryCleaner]:
    yield RepositoryCleaner(git_local_service=git_local_service_fixture)


def test_remove_repositories(
    local_repository_fixture: LocalRepository,
    git_local_service_fixture: MagicMock,
    repository_cleaner_fixture: RepositoryCleaner,
) -> None:

    repository_cleaner_fixture.remove_repositories([local_repository_fixture])

    git_local_service_fixture.remove_repository.assert_called_once_with(local_repository_fixture)


def test_remove_repositories_by_user(
    git_local_service_fixture: MagicMock, repository_cleaner_fixture: RepositoryCleaner
) -> None:

    repository_cleaner_fixture.remove_repositories_by_user(TEST_USERNAME)
    git_local_service_fixture.remove_user_repositories.assert_called_once_with(TEST_USERNAME)
