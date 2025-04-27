from typing import Iterator

import pytest

from git_rank.repositories.git_remote.github_remote_repository import (
    GithubConfig,
    GithubRemoteRepository,
)

MOCK_GITHUB_CONFIG: GithubConfig = {
    "access_token": "MOCK_ACCESS_TOKEN",
    "api_url": "MOCK_API_URL",
    "user_repo_relation": "MOCK_RELATION",
    "results_per_page": 100,
}


@pytest.fixture(name="github_remote_repository_fixture")
def github_remote_repository_fixture() -> Iterator[GithubRemoteRepository]:
    yield GithubRemoteRepository(github_config=MOCK_GITHUB_CONFIG)


def test_get_user_repository_by_url() -> None:
    pass
