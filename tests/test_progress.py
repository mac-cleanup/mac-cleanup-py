"""All tests for mac_cleanup_py.progress"""
from typing import Callable

import pytest
from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from mac_cleanup.progress import ProgressBar


@pytest.mark.parametrize(
    "user_continue",
    [True, False]
)
def test_prompt(
        user_continue: bool,
        capsys: CaptureFixture[str],
        monkeypatch: MonkeyPatch
):
    user_input_str: Callable[..., str] = lambda: "y" if user_continue else "n"

    # Check prompt output
    monkeypatch.setattr("builtins.input", user_input_str)
    assert ProgressBar.prompt("Prompt Text", "Prompt Title") == user_continue

    # Check stdout
    captured = capsys.readouterr()
    assert "Prompt Text" in captured.out
    assert "Prompt Title" in captured.out
