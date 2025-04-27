from typing import Iterator

import os
from unittest.mock import MagicMock, patch

import pytest

from git_rank import STORAGE_DIR
from git_rank.models.local_repository import LocalRepository
from git_rank.models.remote_repository import RemoteRepository
from git_rank.repositories.git_local.git_local_repository import GitLocalRepository

TEST_USERNAME = "TEST_USERNAME"


@pytest.fixture(name="git_local_repository_fixture")
def git_local_repository_fixture() -> Iterator[GitLocalRepository]:
    yield GitLocalRepository()


@patch("git_rank.repositories.git_local.git_local_repository.Repo")
def test_clone_repository(
    remote_repository_fixture: RemoteRepository,
    repo_fixture: MagicMock,
    git_local_repository_fixture: GitLocalRepository,
) -> None:
    with patch("git_rank.repositories.git_local.git_local_repository.Repo", repo_fixture):
        cloned_repository = git_local_repository_fixture.clone_repository(
            remote_repository=remote_repository_fixture
        )

        repo_fixture.clone_from.assert_called_once_with(
            url=remote_repository_fixture.clone_url,
            to_path=os.path.join(
                STORAGE_DIR,
                remote_repository_fixture.user.username,
                remote_repository_fixture.full_name,
            ),
        )

        assert cloned_repository.full_name == remote_repository_fixture.full_name
        assert cloned_repository.user == remote_repository_fixture.user
        assert cloned_repository.repository == repo_fixture.clone_from.return_value


def test_delete_repository(
    git_local_repository_fixture: GitLocalRepository, local_repository_fixture: LocalRepository
) -> None:
    with (
        patch("git_rank.repositories.git_local.git_local_repository.rmtree") as mock_rmtree,
        patch("os.path.exists") as mock_exists,
    ):
        mock_exists.return_value = True
        git_local_repository_fixture.delete_repository(local_repository=local_repository_fixture)

        mock_rmtree.assert_called_once_with(
            str(local_repository_fixture.repository.working_tree_dir)
        )


def test_delete_repositories_by_user(git_local_repository_fixture: GitLocalRepository) -> None:
    with (
        patch("git_rank.repositories.git_local.git_local_repository.rmtree") as mock_rmtree,
        patch("os.path.exists") as mock_exists,
    ):
        mock_exists.return_value = True
        git_local_repository_fixture.delete_repositories_by_user(username=TEST_USERNAME)

        mock_rmtree.assert_called_once_with(os.path.join(STORAGE_DIR, TEST_USERNAME))
