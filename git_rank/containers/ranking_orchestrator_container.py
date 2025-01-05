from dependency_injector import containers, providers

from git_rank.api import api
from git_rank.application.ranking_orchestrator import RankingOrchestrator
from git_rank.application.repository_cloner import RepositoryCloner
from git_rank.containers.service_container import ServiceContainer


class RankingOrchestratorContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(modules=[api])

    service_container = providers.Container(
        ServiceContainer,
        config=config,
    )

    github_repository_cloner = providers.Factory(
        RepositoryCloner,
        git_service=service_container.github_service,
    )

    ranking_orchestrator = providers.Factory(
        RankingOrchestrator, repository_cloner=github_repository_cloner
    )
