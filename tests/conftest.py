import pytest


@pytest.fixture(
    scope="session",
    autouse=False,
)
def get_current_os() -> str:
    import platform

    return platform.system()
