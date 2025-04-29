from typing import Iterator, cast

from unittest.mock import MagicMock, create_autospec

import pytest

from git_rank.application.ranking_orchestrator import RankingOrchestrator
from git_rank.application.repository_cleaner import RepositoryCleaner
from git_rank.application.repository_cloner import RepositoryCloner
from git_rank.application.statistics_analyzer import StatisticsAnalyzer
from git_rank.models.local_repository import LocalRepository
from git_rank.models.statistics.repository_statistics import RepositoryStatistics

TEST_USERNAME = "test-user"
TEST_REPOSITORY_URL = f"https://www.example.com/{TEST_USERNAME}/test-repo.git"


@pytest.fixture(name="repository_cloner_fixture")
def repository_cloner_fixture(local_repository_fixture: LocalRepository) -> MagicMock:
    repository_cloner = cast(MagicMock, create_autospec(RepositoryCloner, instance=True))
    repository_cloner.clone_repositories.return_value = [local_repository_fixture]
    repository_cloner.clone_user_repository.return_value = local_repository_fixture

    return repository_cloner


@pytest.fixture(name="statistics_analyzer_fixture")
def statistics_analyzer_fixture(
    repository_statistics_fixture: RepositoryStatistics,
    cross_repository_statistics_fixture: RepositoryStatistics,
) -> MagicMock:
    statistics_analyzer = cast(MagicMock, create_autospec(StatisticsAnalyzer, instance=True))
    statistics_analyzer.analyze_repository_statistics.return_value = repository_statistics_fixture
    statistics_analyzer.analyze_cross_repository_statistics.return_value = (
        cross_repository_statistics_fixture
    )

    return statistics_analyzer


@pytest.fixture(name="repository_cleaner_fixture")
def repository_cleaner_fixture() -> MagicMock:
    repository_cleaner = cast(MagicMock, create_autospec(RepositoryCleaner, instance=True))

    return repository_cleaner


@pytest.fixture(name="ranking_orchestrator_fixture")
def ranking_orchestrator_fixture(
    repository_cloner_fixture: MagicMock,
    statistics_analyzer_fixture: MagicMock,
    repository_cleaner_fixture: MagicMock,
) -> Iterator[RankingOrchestrator]:
    yield RankingOrchestrator(
        repository_cloner=repository_cloner_fixture,
        statistics_analyzer=statistics_analyzer_fixture,
        repository_cleaner=repository_cleaner_fixture,
    )


def test_rank_user(
    local_repository_fixture: LocalRepository,
    repository_statistics_fixture: RepositoryStatistics,
    cross_repository_statistics_fixture: RepositoryStatistics,
    repository_cloner_fixture: MagicMock,
    statistics_analyzer_fixture: MagicMock,
    repository_cleaner_fixture: MagicMock,
    ranking_orchestrator_fixture: RankingOrchestrator,
) -> None:

    user_statistics = ranking_orchestrator_fixture.rank_user(TEST_USERNAME)

    repository_cloner_fixture.clone_repositories.assert_called_once_with(TEST_USERNAME)

    statistics_analyzer_fixture.analyze_repository_statistics.assert_called_once_with(
        local_repository_fixture
    )
    statistics_analyzer_fixture.analyze_cross_repository_statistics.assert_called_once_with(
        [repository_statistics_fixture]
    )

    repository_cleaner_fixture.remove_repositories_by_user.assert_called_once_with(TEST_USERNAME)

    assert user_statistics.username == TEST_USERNAME
    assert user_statistics.repositories == [repository_statistics_fixture]
    assert user_statistics.cross_repository == cross_repository_statistics_fixture


def test_rank_user_repository(
    local_repository_fixture: LocalRepository,
    repository_statistics_fixture: RepositoryStatistics,
    repository_cloner_fixture: MagicMock,
    statistics_analyzer_fixture: MagicMock,
    repository_cleaner_fixture: MagicMock,
    ranking_orchestrator_fixture: RankingOrchestrator,
) -> None:

    user_statistics = ranking_orchestrator_fixture.rank_user_repository(
        username=TEST_USERNAME, repository_url=TEST_REPOSITORY_URL
    )

    repository_cloner_fixture.clone_user_repository.assert_called_once_with(
        username=TEST_USERNAME, repository_url=TEST_REPOSITORY_URL
    )

    statistics_analyzer_fixture.analyze_repository_statistics.assert_called_once_with(
        local_repository_fixture
    )
    statistics_analyzer_fixture.analyze_cross_repository_statistics.assert_not_called()

    repository_cleaner_fixture.remove_repositories_by_user.assert_called_once_with(TEST_USERNAME)

    assert user_statistics.username == TEST_USERNAME
    assert user_statistics.repositories == [repository_statistics_fixture]
    assert user_statistics.cross_repository is None
