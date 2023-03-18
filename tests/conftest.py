import pytest
from mac_cleanup import Collector


@pytest.fixture(
    scope="session",
    autouse=False
)
def get_current_os(
) -> str:
    import platform

    return platform.system()


@pytest.fixture(
    scope="function",
    autouse=False
)
def get_collector(
) -> Collector:
    return Collector()
