from typing import Iterator

from subprocess import CompletedProcess
from unittest.mock import MagicMock, Mock, patch

import pytest

from git_rank.services.linters.cs_linter import OUTPUT_XML_FILE, CSLinter


@pytest.fixture(name="cs_linter_fixture")
def cs_linter_fixture() -> Iterator[CSLinter]:
    yield CSLinter(linter_config={"arguments": ""})


@patch("git_rank.services.linters.cs_linter.subprocess.run")
def test_lint_commit_file(
    subprocess_run_mock: Mock,
    commit_fixture: MagicMock,
    cs_linter_fixture: CSLinter,
) -> None:

    subprocess_run_mock.side_effect
    cs_linter_fixture.lint_commit_file(commit=commit_fixture, file="test.cs")

    assert subprocess_run_mock.call_count == 2
    assert "dotnet new console" in subprocess_run_mock.call_args_list[0][0]
    assert (
        f"roslynator analyze {cs_linter_fixture.arguments} -o {OUTPUT_XML_FILE}"
        in subprocess_run_mock.call_args_list[1][0]
    )
