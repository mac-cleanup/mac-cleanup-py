from mac_cleanup.core import Path, Command
from mac_cleanup.collector import Collector
from mac_cleanup.console import args
from mac_cleanup.main import main

try:
    from mac_cleanup.__version__ import __version__
except ImportError:  # pragma: no cover
    __version__ = "source"

__title__ = "mac-cleanup-py"
__all__ = [
    "Collector", "Path", "Command", "args",
]
