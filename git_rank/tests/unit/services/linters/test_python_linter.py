from typing import Iterator

from subprocess import CompletedProcess
from unittest.mock import MagicMock, Mock, patch

import pytest

from git_rank.services.linters.python_linter import PythonLinter


@pytest.fixture(name="python_linter_fixture")
def python_linter_fixture() -> Iterator[PythonLinter]:
    yield PythonLinter(linter_config={"arguments": ""})


@patch("git_rank.services.linters.python_linter.subprocess.run")
def test_lint_commit_file(
    subprocess_run_mock: Mock, commit_fixture: MagicMock, python_linter_fixture: PythonLinter
) -> None:

    FINAL_SCORE = 8.5

    subprocess_run_mock.return_value = CompletedProcess(
        args="", stdout=f"Rated at {FINAL_SCORE}/10.\n", returncode=0
    )

    result = python_linter_fixture.lint_commit_file(commit=commit_fixture, file="test.py")

    assert result == FINAL_SCORE
    subprocess_run_mock.assert_called_once()
    assert f"pylint" in subprocess_run_mock.call_args[0][0]


@patch("git_rank.services.linters.python_linter.subprocess.run")
def test_lint_commit_file_empty(
    subprocess_run_mock: Mock, commit_fixture: MagicMock, python_linter_fixture: PythonLinter
) -> None:

    subprocess_run_mock.return_value = CompletedProcess(
        args="", stdout="No rating for empty file.\n", returncode=0
    )

    result = python_linter_fixture.lint_commit_file(commit=commit_fixture, file="test.py")

    assert result == 10
    subprocess_run_mock.assert_called_once()
    assert f"pylint" in subprocess_run_mock.call_args[0][0]
