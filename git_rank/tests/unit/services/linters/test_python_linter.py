from typing import Iterator

from unittest.mock import MagicMock, Mock, patch

import pytest

from git_rank.services.linters.python_linter import PythonLinter


@pytest.fixture(name="python_linter_fixture")
def python_linter_fixture() -> Iterator[PythonLinter]:
    yield PythonLinter(linter_config={"arguments": ""})


@patch("git_rank.services.linters.python_linter.Run")
def test_lint_commit_file(
    pylint_run_mock: Mock, commit_fixture: MagicMock, python_linter_fixture: PythonLinter
) -> None:

    FINAL_SCORE = 8.5

    pylint_run_mock.side_effect = lambda args, reporter, exit: reporter.writeln(
        f"Rated at {FINAL_SCORE}/10.\n"
    )

    result = python_linter_fixture.lint_commit_file(commit=commit_fixture, file="test.py")

    assert result == FINAL_SCORE
    pylint_run_mock.assert_called_once()


@patch("git_rank.services.linters.python_linter.Run")
def test_lint_commit_file_empty(
    pylint_run_mock: Mock, commit_fixture: MagicMock, python_linter_fixture: PythonLinter
) -> None:

    pylint_run_mock.side_effect = lambda args, reporter, exit: reporter.writeln(
        f"No rating for empty file.\n"
    )

    result = python_linter_fixture.lint_commit_file(commit=commit_fixture, file="test.py")

    assert result == 10
    pylint_run_mock.assert_called_once()
