from typing import cast

from unittest.mock import MagicMock, create_autospec

import pytest
from git import Commit, Repo

from tests.fixtures.user_data_fixtures import TEST_USER_EMAIL, TEST_USER_NAME


@pytest.fixture(name="commit_fixture")
def commit_fixture() -> MagicMock:
    commit = cast(MagicMock, create_autospec(Commit, instance=True))
    commit.author.name = TEST_USER_NAME
    commit.author.email = TEST_USER_EMAIL

    return commit


@pytest.fixture(name="commit_another_author_fixture")
def commit_another_author_fixture() -> MagicMock:
    commit = cast(MagicMock, create_autospec(Commit, instance=True))
    commit.author.name = "NOT" + TEST_USER_NAME
    commit.author.email = "NOT" + TEST_USER_EMAIL

    return commit


@pytest.fixture(name="repo_fixture")
def repo_fixture(commit_fixture: MagicMock, commit_another_author_fixture: MagicMock) -> MagicMock:
    repo = cast(MagicMock, create_autospec(Repo, instance=True))
    repo.clone_from.return_value = repo
    repo.iter_commits.return_value = [commit_fixture, commit_another_author_fixture]

    return repo
