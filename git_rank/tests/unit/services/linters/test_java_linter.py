from typing import Iterator

from subprocess import CompletedProcess
from unittest.mock import MagicMock, Mock, patch

import pytest

from git_rank.services.linters.java_linter import JavaLinter


@pytest.fixture(name="java_linter_fixture")
def java_linter_fixture() -> Iterator[JavaLinter]:
    yield JavaLinter(linter_config={"arguments": ""})


@patch("git_rank.services.linters.java_linter.subprocess.run")
def test_lint_commit_file(
    subprocess_run_mock: Mock,
    commit_fixture: MagicMock,
    java_linter_fixture: JavaLinter,
) -> None:

    subprocess_run_mock.return_value = CompletedProcess(
        args="", stdout='{"files": [{"violations": [{"priority": 5}]}]}', returncode=0
    )

    result = java_linter_fixture.lint_commit_file(commit=commit_fixture, file="test.java")

    assert result != 10 and result != 0.0
    subprocess_run_mock.assert_called_once()
    assert "pmd check" in subprocess_run_mock.call_args[0][0]


@patch("git_rank.services.linters.java_linter.subprocess.run")
def test_lint_commit_file_empty(
    subprocess_run_mock: Mock,
    commit_fixture: MagicMock,
    java_linter_fixture: JavaLinter,
) -> None:

    subprocess_run_mock.return_value = CompletedProcess(
        args="", stdout='{"files": []}', returncode=0
    )

    result = java_linter_fixture.lint_commit_file(commit=commit_fixture, file="test.java")
    subprocess_run_mock.assert_called_once()
    assert "pmd check" in subprocess_run_mock.call_args[0][0]
    assert result == 10.0
