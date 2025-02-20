from dependency_injector import containers, providers

from git_rank.repositories.git_local.git_local_repository import GitLocalRepository
from git_rank.repositories.git_remote.github_remote_repository import GithubRemoteRepository


class RepositoryContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    github_remote_repository = providers.Factory(
        GithubRemoteRepository, github_config=config.git_remote.github
    )

    git_local_repository = providers.Factory(
        GitLocalRepository,
    )
