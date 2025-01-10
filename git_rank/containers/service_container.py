from dependency_injector import containers, providers

from git_rank.containers.repository_container import RepositoryContainer
from git_rank.services.git_local_service import GitLocalService
from git_rank.services.git_remote_service import GitRemoteService


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    repository_container = providers.Container(
        RepositoryContainer,
        config=config,
    )

    github_remote_service = providers.Factory(
        GitRemoteService,
        git_remote_repository=repository_container.github_remote_repository,
    )

    git_local_service = providers.Factory(
        GitLocalService,
        git_local_repository=repository_container.git_local_repository,
    )
