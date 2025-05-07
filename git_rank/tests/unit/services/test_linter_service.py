from typing import Iterator, cast

from unittest.mock import MagicMock, create_autospec

import pytest

from git_rank.models.statistics.technology_statistics import TechnologyType
from git_rank.services.linter_service import LinterService
from git_rank.services.linters.cs_linter import CSLinter
from git_rank.services.linters.java_linter import JavaLinter
from git_rank.services.linters.python_linter import PythonLinter

PYTHON_LINTER_SCORE = 8.0
JAVA_LINTER_SCORE = 9.0
CS_LINTER_SCORE = 10.0

TEST_FILE_PATH = "/path/to/test_file"


@pytest.fixture(name="python_linter_fixture")
def python_linter_fixture() -> MagicMock:
    python_linter = cast(MagicMock, create_autospec(PythonLinter, instance=True))

    python_linter.lint_commit_file.return_value = PYTHON_LINTER_SCORE
    return python_linter


@pytest.fixture(name="java_linter_fixture")
def java_linter_fixture() -> MagicMock:
    java_linter = cast(MagicMock, create_autospec(JavaLinter, instance=True))

    java_linter.lint_commit_file.return_value = JAVA_LINTER_SCORE
    return java_linter


@pytest.fixture(name="cs_linter_fixture")
def cs_linter_fixture() -> MagicMock:
    cs_linter = cast(MagicMock, create_autospec(CSLinter, instance=True))

    cs_linter.lint_commit_file.return_value = CS_LINTER_SCORE
    return cs_linter


@pytest.fixture(name="linter_service_fixture")
def linter_service_fixture(
    python_linter_fixture: MagicMock,
    java_linter_fixture: MagicMock,
    cs_linter_fixture: MagicMock,
) -> Iterator[LinterService]:
    yield LinterService(
        python_linter=python_linter_fixture,
        java_linter=java_linter_fixture,
        cs_linter=cs_linter_fixture,
    )


def test_lint_commit_file_python(
    python_linter_fixture: MagicMock,
    java_linter_fixture: MagicMock,
    cs_linter_fixture: MagicMock,
    commit_fixture: MagicMock,
    linter_service_fixture: LinterService,
) -> None:

    python_result = linter_service_fixture.lint_commit_file(
        commit=commit_fixture, file=TEST_FILE_PATH, technology=TechnologyType.PYTHON
    )

    assert python_result == PYTHON_LINTER_SCORE
    python_linter_fixture.lint_commit_file.assert_called_once_with(commit_fixture, TEST_FILE_PATH)
    java_linter_fixture.lint_commit_file.assert_not_called()
    cs_linter_fixture.lint_commit_file.assert_not_called()


def test_lint_commit_file_java(
    python_linter_fixture: MagicMock,
    java_linter_fixture: MagicMock,
    cs_linter_fixture: MagicMock,
    commit_fixture: MagicMock,
    linter_service_fixture: LinterService,
) -> None:

    java_result = linter_service_fixture.lint_commit_file(
        commit=commit_fixture, file=TEST_FILE_PATH, technology=TechnologyType.JAVA
    )

    assert java_result == JAVA_LINTER_SCORE
    java_linter_fixture.lint_commit_file.assert_called_once_with(commit_fixture, TEST_FILE_PATH)
    python_linter_fixture.lint_commit_file.assert_not_called()
    cs_linter_fixture.lint_commit_file.assert_not_called()


def test_lint_commit_file_cs(
    python_linter_fixture: MagicMock,
    java_linter_fixture: MagicMock,
    cs_linter_fixture: MagicMock,
    commit_fixture: MagicMock,
    linter_service_fixture: LinterService,
) -> None:

    cs_result = linter_service_fixture.lint_commit_file(
        commit=commit_fixture, file=TEST_FILE_PATH, technology=TechnologyType.CS
    )

    assert cs_result == CS_LINTER_SCORE
    cs_linter_fixture.lint_commit_file.assert_called_once_with(commit_fixture, TEST_FILE_PATH)
    python_linter_fixture.lint_commit_file.assert_not_called()
    java_linter_fixture.lint_commit_file.assert_not_called()


def test_lint_commit_file_other(
    python_linter_fixture: MagicMock,
    java_linter_fixture: MagicMock,
    cs_linter_fixture: MagicMock,
    commit_fixture: MagicMock,
    linter_service_fixture: LinterService,
) -> None:

    other_result = linter_service_fixture.lint_commit_file(
        commit=commit_fixture, file=TEST_FILE_PATH, technology=TechnologyType.OTHER
    )

    assert other_result == 0
    python_linter_fixture.lint_commit_file.assert_not_called()
    java_linter_fixture.lint_commit_file.assert_not_called()
    cs_linter_fixture.lint_commit_file.assert_not_called()
