from typing import TypedDict

import requests
from structlog import get_logger

from git_rank.models.remote_repository import RemoteRepository
from git_rank.repositories.git_remote.abstract_git_remote_repository import (
    AbstractGitRemoteRepository,
)

logger = get_logger()


class GithubConfig(TypedDict):
    access_token: str
    api_url: str
    user_repo_relation: str
    results_per_page: int


class GithubRemoteRepository(AbstractGitRemoteRepository):

    def __init__(self, github_config: GithubConfig) -> None:
        self.access_token = github_config["access_token"]
        self.api_url = github_config["api_url"]
        self.user_repo_relation = github_config["user_repo_relation"]
        self.results_per_page = github_config["results_per_page"]

    def get_repositories_by_user(self, username: str) -> list[RemoteRepository]:
        log = logger.bind(username=username)
        log.debug("get_repositories_by_user.start")

        user_name = self._get_github_user_name(username)

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
                # TODO Custom Exceptions
                raise Exception("Error fetching user repositories")

            repositories_page_json = repositories_page.json()

            if not len(repositories_page_json):
                break

            remote_repositories += list(
                map(
                    lambda remote_repository: RemoteRepository(
                        clone_url=remote_repository["clone_url"],
                        full_name=remote_repository["full_name"],
                        username=username,
                        user_name=user_name,
                    ),
                    repositories_page_json,
                )
            )
            page += 1

        log.debug("get_repositories_by_user.end", repositories=remote_repositories)
        return remote_repositories

    def _get_github_user_name(self, username: str) -> str:
        return str(
            requests.get(
                url=f"{self.api_url}/users/{username}",
                headers={
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"Bearer {self.access_token}",
                },
            ).json()["name"]
        )
