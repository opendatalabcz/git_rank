from typing import cast

from unittest.mock import MagicMock, create_autospec

import pytest
from git import Repo


@pytest.fixture(name="repo_fixture")
def repo_fixture() -> MagicMock:
    repo = cast(MagicMock, create_autospec(Repo, instance=True))
    repo.clone_from.return_value = repo

    return repo
