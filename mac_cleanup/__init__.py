from .console import args
from .utils import Collector
from .cli import main

try:
    from __version__ import __version__
except ImportError:
    __version__ = "source"

__title__ = "mac-cleanup-py"
__all__ = [
    "Collector", "args",
]
