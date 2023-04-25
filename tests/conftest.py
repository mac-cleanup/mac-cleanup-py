import pytest
from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture()
def _command_with_root(monkeypatch: MonkeyPatch) -> None:  # pyright: ignore [reportUnusedFunction]
    """Simulate user has root."""

    monkeypatch.setattr("mac_cleanup.core_modules.Command._BaseCommand__has_root", True)


@pytest.fixture()
def _path_with_root(monkeypatch: MonkeyPatch) -> None:  # pyright: ignore [reportUnusedFunction]
    """Simulate user has root."""

    monkeypatch.setattr("mac_cleanup.core_modules.Path._BaseCommand__has_root", True)
