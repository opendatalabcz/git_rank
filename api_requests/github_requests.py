import os
import sys
from enum import Enum

import requests

GITHUB_API_URL = "https://api.github.com"
AUTH_TOKEN = os.getenv("ACCESS_TOKEN")
REQUESTS_HEADERS = {'Accept': 'application/vnd.github+json', 'Authorization': f'Bearer {AUTH_TOKEN}'}
RESULTS_PER_PAGE = 100


class RepositoriesRelationship(Enum):
    ALL = "all",
    MEMBER = "member",
    OWNER = "owner"


def get_repositories(username: str, relationship: RepositoriesRelationship):
    page = 1
    repositories = []
    while True:
        repositories_page = requests.get(
            url=f"{GITHUB_API_URL}/users/{username}/repos",
            params={
                "page": page,
                "per_page": RESULTS_PER_PAGE,
                "type": relationship,
            },
            headers=REQUESTS_HEADERS,
        ).json()

        if not len(repositories_page):
            break

        repositories += list(map(lambda repository: repository["full_name"], repositories_page))
        page += 1

    print("Found repositories: " + ", ".join(repositories))
    return repositories


def get_commits_in_repository(username: str, repository: str):
    page = 1
    commits = []
    while True:
        commits_page = requests.get(
            url=f"{GITHUB_API_URL}/repos/{repository}/commits",
            params={"page": page,
                    "per_page": RESULTS_PER_PAGE,
                    "author": username,
                    "commiter": username
                    },
            headers=REQUESTS_HEADERS,
        ).json()

        if not len(commits_page):
            break

        commits += list(map(lambda commit: commit["sha"], commits_page))
        page += 1

    print(f"Found {len(commits)} commits in {repository} repository: " + ", ".join(commits))
    return commits


def get_changes_in_commit(repository: str, ref: str):
    page = 1
    changes = []
    while True:
        changes_page = requests.get(
            url=f"{GITHUB_API_URL}/repos/{repository}/commits/{ref}",
            params={
                "page": page,
                "per_page": RESULTS_PER_PAGE,
            },
            headers=REQUESTS_HEADERS,
        ).json()["files"]

        if not len(changes_page):
            break

        changes += list(map(lambda change: change["patch"][:10], changes_page))
        page += 1

    print(f"Found {len(changes)} changes in {ref} commit:\n" + "\n".join(changes))


def get_user_activity(username: str):
    repositories = get_repositories(username=username, relationship=RepositoriesRelationship.ALL)
    for repository in repositories:
        commits = get_commits_in_repository(username=username, repository=repository)
        for commit in commits:
            get_changes_in_commit(repository=repository, ref=commit)


if __name__ == "__main__":
    get_user_activity(sys.argv[1])
