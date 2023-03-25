from mac_cleanup.core import ProxyCollector as Collector
from mac_cleanup.core_modules import Path, Command
from mac_cleanup.parser import args
from mac_cleanup.main import main

try:
    from mac_cleanup.__version__ import __version__
except ImportError:
    __version__ = "source"

__title__ = "mac-cleanup-py"
__all__ = [
    "Collector", "Path", "Command", "args", "main"
]
