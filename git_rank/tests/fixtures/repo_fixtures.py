from typing import cast

from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, create_autospec

import pytest
from git import Commit, Repo

from tests.fixtures.user_data_fixtures import TEST_USER_EMAIL, TEST_USER_NAME


@pytest.fixture(name="commit_tree_fixture")
def commit_tree_fixture() -> MagicMock:
    commit_tree = MagicMock()
    file = MagicMock()
    data_stream = MagicMock()

    data_stream.read.return_value = b"print('Hello World')\n\n\n\n\n\n\n\n\n\n"
    file.data_stream = data_stream
    commit_tree.__getitem__.return_value = file

    return commit_tree


@pytest.fixture(name="commit_fixture")
def commit_fixture(
    commit_tree_fixture: MagicMock, commit_another_author_fixture: Commit
) -> MagicMock:
    commit = cast(MagicMock, create_autospec(Commit, instance=True))
    commit.author.name = TEST_USER_NAME
    commit.author.email = TEST_USER_EMAIL
    commit.tree = commit_tree_fixture
    commit.stats.files = {
        Path("/path/to/added_file.py"): {
            "change_type": "A",
            "lines": 10,
            "insertions": 10,
            "deletions": 0,
        },
        Path("/path/to/modified_file.py"): {
            "change_type": "M",
            "lines": 20,
            "insertions": 15,
            "deletions": 5,
        },
    }
    commit.parents = [commit_another_author_fixture]
    commit.hexsha = "TEST_COMMIT_SHA"
    commit.committed_date = datetime(2000, 12, 1, 12, 13, 14).timestamp()

    return commit


@pytest.fixture(name="commit_another_author_fixture")
def commit_another_author_fixture(commit_tree_fixture: MagicMock) -> MagicMock:
    commit = cast(MagicMock, create_autospec(Commit, instance=True))
    commit.author.name = "NOT" + TEST_USER_NAME
    commit.author.email = "NOT" + TEST_USER_EMAIL
    commit.tree = commit_tree_fixture

    return commit


@pytest.fixture(name="repo_fixture")
def repo_fixture(commit_fixture: MagicMock, commit_another_author_fixture: MagicMock) -> MagicMock:
    repo = cast(MagicMock, create_autospec(Repo, instance=True))
    repo.clone_from.return_value = repo
    repo.iter_commits.return_value = [commit_fixture, commit_another_author_fixture]

    return repo
