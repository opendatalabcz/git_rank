from dependency_injector import containers, providers

from git_rank.containers.repository_container import RepositoryContainer
from git_rank.services.git_local_service import GitLocalService
from git_rank.services.git_remote_service import GitRemoteService
from git_rank.services.linter_service import LinterService
from git_rank.services.linters.cs_linter import CSLinter
from git_rank.services.linters.java_linter import JavaLinter
from git_rank.services.linters.python_linter import PythonLinter


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

    linter_service = providers.Factory(
        LinterService,
        python_linter=providers.Factory(PythonLinter, linter_config=config.linters.python),
        java_linter=providers.Factory(JavaLinter, linter_config=config.linters.java),
        cs_linter=providers.Factory(CSLinter, linter_config=config.linters.cs),
    )
