from typing import Iterator

import json
from unittest.mock import MagicMock, patch

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
USERNAME = "test-user"
REPOSITORY_NAME = "test-repo"
REPOSITORY_URL = f"https://www.github.com/{USERNAME}/{REPOSITORY_NAME}.git"
GITHUB_USER_NAME = "test-user-name"
GITHUB_USER_EMAIL = "test-user-email"


@pytest.fixture(name="github_remote_repository_fixture")
def github_remote_repository_fixture() -> Iterator[GithubRemoteRepository]:
    yield GithubRemoteRepository(github_config=MOCK_GITHUB_CONFIG)


@patch("git_rank.repositories.git_remote.github_remote_repository.requests.get")
def test_get_user_repository_by_url(
    requests_get_mock: MagicMock, github_remote_repository_fixture: GithubRemoteRepository
) -> None:

    requests_get_mock.return_value.status_code = 200
    requests_get_mock.return_value.json.return_value = json.loads(
        f'{{"name": "{GITHUB_USER_NAME}", "email": "{GITHUB_USER_EMAIL}"}}'
    )

    repository = github_remote_repository_fixture.get_user_repository_by_url(
        username=USERNAME, repository_url=REPOSITORY_URL
    )

    requests_get_mock.assert_called_once_with(
        url=f"{MOCK_GITHUB_CONFIG['api_url']}/users/{USERNAME}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {MOCK_GITHUB_CONFIG['access_token']}",
        },
    )

    assert repository.clone_url == REPOSITORY_URL
    assert repository.full_name == REPOSITORY_NAME
    assert repository.user.username == USERNAME
    assert repository.user.user_name == GITHUB_USER_NAME
    assert repository.user.user_email == GITHUB_USER_EMAIL


@patch("git_rank.repositories.git_remote.github_remote_repository.requests.get")
def test_get_repositories_by_user(
    requests_get_mock: MagicMock, github_remote_repository_fixture: GithubRemoteRepository
) -> None:

    user_data_request = MagicMock()
    user_data_request.status_code = 200
    user_data_request.json.return_value = json.loads(
        f'{{"name": "{GITHUB_USER_NAME}", "email": "{GITHUB_USER_EMAIL}"}}'
    )

    user_repos_request = MagicMock()
    user_repos_request.status_code = 200
    user_repos_request.json.return_value = json.loads(
        f'[{{"clone_url": "{REPOSITORY_URL}", "full_name": "{REPOSITORY_NAME}"}}]'
    )

    user_repos_empty_request = MagicMock()
    user_repos_empty_request.status_code = 200
    user_repos_empty_request.json.return_value = json.loads("[]")

    requests_get_mock.side_effect = [
        user_data_request,
        user_repos_request,
        user_repos_empty_request,
    ]

    repositories = github_remote_repository_fixture.get_repositories_by_user(username=USERNAME)

    requests_get_mock.call_count == 3
    requests_get_mock.assert_any_call(
        url=f"{MOCK_GITHUB_CONFIG['api_url']}/users/{USERNAME}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {MOCK_GITHUB_CONFIG['access_token']}",
        },
    )
    requests_get_mock.assert_any_call(
        url=f"{MOCK_GITHUB_CONFIG['api_url']}/users/{USERNAME}/repos",
        params={
            "page": "1",
            "per_page": str(MOCK_GITHUB_CONFIG["results_per_page"]),
            "type": MOCK_GITHUB_CONFIG["user_repo_relation"],
        },
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {MOCK_GITHUB_CONFIG['access_token']}",
        },
    )
    requests_get_mock.assert_any_call(
        url=f"{MOCK_GITHUB_CONFIG['api_url']}/users/{USERNAME}/repos",
        params={
            "page": "2",
            "per_page": str(MOCK_GITHUB_CONFIG["results_per_page"]),
            "type": MOCK_GITHUB_CONFIG["user_repo_relation"],
        },
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {MOCK_GITHUB_CONFIG['access_token']}",
        },
    )

    assert len(repositories) == 1
    assert repositories[0].clone_url == REPOSITORY_URL
    assert repositories[0].full_name == REPOSITORY_NAME
    assert repositories[0].user.username == USERNAME
    assert repositories[0].user.user_name == GITHUB_USER_NAME
    assert repositories[0].user.user_email == GITHUB_USER_EMAIL
