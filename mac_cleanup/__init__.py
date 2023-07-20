from mac_cleanup.parser import args  # isort: skip_file
from mac_cleanup.core import ProxyCollector as Collector
from mac_cleanup.core_modules import Command, Path
from mac_cleanup.main import EntryPoint

try:
    from mac_cleanup.__version__ import __version__
except ImportError:  # pragma: no cover
    __version__ = "source"

main = EntryPoint().start

__title__ = "mac-cleanup-py"
__all__ = ["Collector", "Path", "Command", "args", "main"]
