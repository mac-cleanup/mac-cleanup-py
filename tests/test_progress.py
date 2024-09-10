"""All tests for mac_cleanup_py.progress."""

from typing import Callable

import pytest
from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from mac_cleanup.progress import ProgressBar


@pytest.mark.parametrize("user_continue", [True, False])
def test_prompt(user_continue: bool, capsys: CaptureFixture[str], monkeypatch: MonkeyPatch):
    """Test ProgressBar prompt call."""

    # Dummy user input
    user_input_str: Callable[..., str] = lambda: "y" if user_continue else "n"

    # Check prompt output
    monkeypatch.setattr("builtins.input", user_input_str)
    assert ProgressBar.prompt("Prompt Text", "Prompt Title") == user_continue

    # Check stdout
    captured = capsys.readouterr().out
    assert "Prompt Text" in captured
    assert "Prompt Title" in captured


def test_wrap_iter(capsys: CaptureFixture[str], monkeypatch: MonkeyPatch):
    """Test ProgressBar wrap_iter call."""

    seq = list(range(5))

    for _ in ProgressBar.wrap_iter(seq, total=len(seq), description="test_wrap_iter"):
        # Change transient attribute to be able to capture stdout
        monkeypatch.setattr(ProgressBar.current_progress.live, "transient", False)

    # Check stdout
    captured = capsys.readouterr().out

    # Check percents in output
    assert "100%" in captured

    # Check description in output
    assert "test_wrap_iter" in captured
