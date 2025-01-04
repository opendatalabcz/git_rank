from dependency_injector import containers, providers

from git_rank.api import api
from git_rank.application.ranking_orchestrator import RankingOrchestrator
from git_rank.application.repository_cloner import RepositoryCloner


class RankingOrchestratorContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(modules=[api])

    repository_cloner = providers.Factory(
        RepositoryCloner,
    )

    ranking_orchestrator = providers.Factory(
        RankingOrchestrator, repository_cloner=repository_cloner
    )
