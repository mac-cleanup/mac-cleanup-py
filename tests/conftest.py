import pytest
from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture(scope="session", autouse=False)
def get_current_os() -> str:
    import platform

    return platform.system()


@pytest.fixture
def command_with_root(monkeypatch: MonkeyPatch) -> None:
    """Simulate user has root"""

    monkeypatch.setattr("mac_cleanup.core_modules.Command._BaseCommand__has_root", True)


@pytest.fixture
def path_with_root(monkeypatch: MonkeyPatch) -> None:
    """Simulate user has root"""

    monkeypatch.setattr("mac_cleanup.core_modules.Path._BaseCommand__has_root", True)
