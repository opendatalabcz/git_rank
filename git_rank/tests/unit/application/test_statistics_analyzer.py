from typing import Iterator, cast

from datetime import datetime
from unittest.mock import MagicMock, call, create_autospec

import pytest
from git import Commit

from git_rank.application.statistics_analyzer import StatisticsAnalyzer
from git_rank.constants.git_rank_constants import GitRankConstants
from git_rank.models.local_repository import LocalRepository
from git_rank.models.statistics.file_statistics import FileState
from git_rank.models.statistics.repository_statistics import RepositoryStatistics
from git_rank.models.statistics.technology_statistics import TechnologyType
from git_rank.services.git_local_service import GitLocalService
from git_rank.services.linter_service import LinterService

TEST_LINTER_SCORE = 5.0


@pytest.fixture(name="git_local_service_fixture")
def git_local_service_fixture(commit_fixture: Commit) -> MagicMock:
    git_local_service = cast(MagicMock, create_autospec(GitLocalService, instance=True))
    git_local_service.filter_user_commits.return_value = [commit_fixture]

    return git_local_service


@pytest.fixture(name="linter_service_fixture")
def linter_service_fixture() -> MagicMock:
    linter_service = cast(MagicMock, create_autospec(LinterService, instance=True))
    linter_service.lint_commit_file.return_value = TEST_LINTER_SCORE

    return linter_service


@pytest.fixture(name="statistics_analyzer_fixture")
def statistics_analyzer_fixture(
    git_local_service_fixture: MagicMock, linter_service_fixture: MagicMock
) -> Iterator[StatisticsAnalyzer]:
    yield StatisticsAnalyzer(
        git_local_service=git_local_service_fixture, linter_service=linter_service_fixture
    )


def test_analyze_repository_statistics(
    local_repository_fixture: LocalRepository,
    commit_fixture: Commit,
    git_local_service_fixture: MagicMock,
    linter_service_fixture: MagicMock,
    statistics_analyzer_fixture: StatisticsAnalyzer,
) -> None:

    repository_statistics = statistics_analyzer_fixture.analyze_repository_statistics(
        local_repository=local_repository_fixture
    )

    git_local_service_fixture.filter_user_commits.assert_called_once_with(local_repository_fixture)

    assert (
        linter_service_fixture.lint_commit_file.call_count == len(commit_fixture.stats.files) + 1
    )  # One file is modified, so it has two calls (parent linting)
    linter_service_fixture.lint_commit_file.assert_has_calls(
        [
            call(
                commit=commit_fixture,
                file=list(commit_fixture.stats.files.keys())[0],
                technology=TechnologyType.PYTHON,
            ),
            call(
                commit=commit_fixture,
                file=list(commit_fixture.stats.files.keys())[1],
                technology=TechnologyType.PYTHON,
            ),
            call(
                commit=commit_fixture.parents[0],
                file=list(commit_fixture.stats.files.keys())[1],
                technology=TechnologyType.PYTHON,
            ),
        ]
    )

    # Assertions for RepositoryStatistics
    assert repository_statistics.repository_name == local_repository_fixture.full_name
    assert repository_statistics.total_commits == len(
        list(local_repository_fixture.repository.iter_commits())
    )
    assert repository_statistics.user_commits == len(
        git_local_service_fixture.filter_user_commits(local_repository_fixture)
    )

    # Assertions for CommitStatistics
    assert len(repository_statistics.commits) == len(
        git_local_service_fixture.filter_user_commits(local_repository_fixture)
    )
    assert repository_statistics.commits[0].commit_sha == commit_fixture.hexsha
    assert repository_statistics.commits[0].commit_date == datetime.fromtimestamp(
        commit_fixture.committed_date
    )
    assert repository_statistics.commits[0].average_add_lint_score == TEST_LINTER_SCORE
    assert (
        repository_statistics.commits[0].average_change_lint_score
        == TEST_LINTER_SCORE - TEST_LINTER_SCORE
    )

    # Assertions for FileStatistics (added file)
    assert repository_statistics.commits[0].files[0].file_name == str(
        list(commit_fixture.stats.files.keys())[0]
    )
    assert repository_statistics.commits[0].files[0].file_state == FileState.ADDED
    assert repository_statistics.commits[0].files[0].lint_score == TEST_LINTER_SCORE
    assert repository_statistics.commits[0].files[0].technology == TechnologyType.PYTHON

    # Assertions for FileStatistics (modified file)
    assert repository_statistics.commits[0].files[1].file_name == str(
        list(commit_fixture.stats.files.keys())[1]
    )
    assert repository_statistics.commits[0].files[1].file_state == FileState.CHANGED
    assert (
        repository_statistics.commits[0].files[1].lint_score
        == TEST_LINTER_SCORE - TEST_LINTER_SCORE
    )
    assert repository_statistics.commits[0].files[1].technology == TechnologyType.PYTHON

    # Assertions for TechnologyStatistics
    assert len(repository_statistics.technologies) == 1
    assert repository_statistics.technologies[0].technology == TechnologyType.PYTHON
    assert repository_statistics.technologies[0].total_changes == len(commit_fixture.stats.files)
    assert repository_statistics.technologies[0].first_used_date == datetime.fromtimestamp(
        commit_fixture.committed_date
    )
    assert repository_statistics.technologies[0].last_used_date == datetime.fromtimestamp(
        commit_fixture.committed_date
    )
    assert repository_statistics.technologies[0].weeks_used == 1


def test_analyze_cross_repository_statistics(
    repository_statistics_fixture: RepositoryStatistics,
    statistics_analyzer_fixture: StatisticsAnalyzer,
) -> None:
    repository_statistics_list = [repository_statistics_fixture, repository_statistics_fixture]

    cross_repository_statistics = statistics_analyzer_fixture.analyze_cross_repository_statistics(
        user_repositories_statistics=repository_statistics_list
    )

    assert cross_repository_statistics is not None
    assert cross_repository_statistics.repository_name == GitRankConstants.CROSS_REPOSITORY_NAME
    assert cross_repository_statistics.total_commits == sum(
        repository_statistics.total_commits for repository_statistics in repository_statistics_list
    )
    assert cross_repository_statistics.user_commits == sum(
        repository_statistics.user_commits for repository_statistics in repository_statistics_list
    )
    assert cross_repository_statistics.commits == sum(
        [repository_statistics.commits for repository_statistics in repository_statistics_list], []
    )
    assert cross_repository_statistics.technologies == sum(
        [
            repository_statistics.technologies
            for repository_statistics in repository_statistics_list
        ],
        [],
    )
