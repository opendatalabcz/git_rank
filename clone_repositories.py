import os
import sys
from enum import Enum
from git import Repo

import requests

ROOT_DIR = os.path.dirname(__file__)
STORAGE_DIR = os.path.join(ROOT_DIR, "storage")

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

        repositories += list(map(lambda repository: {"url": repository["clone_url"], "name": repository["full_name"]}, repositories_page))
        page += 1

    print("Found repositories:\n" + "\n".join(map(lambda repository: repository["name"], repositories)))
    return repositories


def clone_user_repositories(username: str):
    repositories = get_repositories(username=username, relationship=RepositoriesRelationship.OWNER)
    for repository in repositories:
        Repo.clone_from(repository["url"], os.path.join(STORAGE_DIR, repository["name"]))

if __name__ == "__main__":
    clone_user_repositories(sys.argv[1])
