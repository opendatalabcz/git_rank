from dependency_injector import containers, providers

from git_rank.api import api
from git_rank.application.ranking_orchestrator import RankingOrchestrator
from git_rank.application.repository_cleaner import RepositoryCleaner
from git_rank.application.repository_cloner import RepositoryCloner
from git_rank.application.statistics_analyzer import StatisticsAnalyzer
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
        git_remote_service=service_container.github_remote_service,
        git_local_service=service_container.git_local_service,
    )

    statistics_analyzer = providers.Factory(
        StatisticsAnalyzer,
        git_local_service=service_container.git_local_service,
        linter_service=service_container.linter_service,
    )

    repository_cleaner = providers.Factory(
        RepositoryCleaner,
        git_local_service=service_container.git_local_service,
    )

    ranking_orchestrator = providers.Factory(
        RankingOrchestrator,
        repository_cloner=github_repository_cloner,
        statistics_analyzer=statistics_analyzer,
        repository_cleaner=repository_cleaner,
    )
