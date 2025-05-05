from typing import Any, TypedDict

import requests
from structlog import get_logger

from git_rank.models.remote_repository import RemoteRepository
from git_rank.models.user_data import UserData
from git_rank.repositories.git_remote.abstract_git_remote_repository import (
    AbstractGitRemoteRepository,
)

logger = get_logger()


class GithubConfig(TypedDict):
    """Configuration for Github API access."""

    access_token: str
    api_url: str
    user_repo_relation: str
    results_per_page: int


class GithubRemoteRepository(AbstractGitRemoteRepository):
    """GitHub platform implementation."""

    def __init__(self, github_config: GithubConfig) -> None:
        self.access_token = github_config["access_token"]
        self.api_url = github_config["api_url"]
        self.user_repo_relation = github_config["user_repo_relation"]
        self.results_per_page = github_config["results_per_page"]

    def get_repositories_by_user(self, username: str) -> list[RemoteRepository]:
        log = logger.bind(username=username)
        log.debug("get_repositories_by_user.start")

        user_data = self._get_github_user_data(username)

        page = 1
        remote_repositories = []
        while True:
            repositories_page = requests.get(
                url=f"{self.api_url}/users/{username}/repos",
                params={
                    "page": str(page),
                    "per_page": str(self.results_per_page),
                    "type": self.user_repo_relation,
                },
                headers={
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"Bearer {self.access_token}",
                },
            )

            if repositories_page.status_code != 200:
                log.error(
                    "Error fetching user repositories",
                    status_code=repositories_page.status_code,
                    reason=repositories_page.reason,
                )
                raise Exception("Error fetching user repositories")

            repositories_page_json = repositories_page.json()

            if not len(repositories_page_json):
                break

            remote_repositories += list(
                map(
                    lambda remote_repository: RemoteRepository(
                        clone_url=remote_repository["clone_url"],
                        full_name=remote_repository["full_name"],
                        user=user_data,
                    ),
                    repositories_page_json,
                )
            )
            page += 1

        log.debug("get_repositories_by_user.end", repositories=remote_repositories)
        return remote_repositories

    def get_user_repository_by_url(self, username: str, repository_url: str) -> RemoteRepository:
        repository = super().get_user_repository_by_url(
            username=username, repository_url=repository_url
        )
        try:
            user_data = self._get_github_user_data(username)
            repository.user = user_data
        except Exception as e:
            logger.warning("Error fetching user data from GitHub.", username=username)

        return repository

    def _get_github_user_data(self, username: str) -> UserData:
        """Fetches user data from Github API."""

        user_data = requests.get(
            url=f"{self.api_url}/users/{username}",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        if user_data.status_code != 200:
            logger.error(
                "Error fetching user data",
                status_code=user_data.status_code,
                reason=user_data.reason,
            )
            raise Exception("Error fetching user data")

        user_data_json: dict[str, Any] = user_data.json()

        return UserData(
            username=username,
            user_name=user_data_json["name"],
            user_email=user_data_json["email"],
        )
