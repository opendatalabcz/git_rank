from dependency_injector import containers, providers

from git_rank.services.git.github_service import GithubService


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    github_service = providers.Factory(
        GithubService, github_config=config.git_remote.github
    )
