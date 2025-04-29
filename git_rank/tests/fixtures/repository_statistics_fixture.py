import pytest

from git_rank.constants.git_rank_constants import GitRankConstants
from git_rank.models.statistics.repository_statistics import RepositoryStatistics


@pytest.fixture(name="repository_statistics_fixture")
def repository_statistics_fixture() -> RepositoryStatistics:
    return RepositoryStatistics(
        repository_name="TEST_REPOSITORY_NAME", user_commits=100, technologies=[], commits=[]
    )


@pytest.fixture(name="cross_repository_statistics_fixture")
def cross_repository_statistics_fixture() -> RepositoryStatistics:
    return RepositoryStatistics(
        repository_name=GitRankConstants.CROSS_REPOSITORY_NAME,
        user_commits=100,
        technologies=[],
        commits=[],
    )
