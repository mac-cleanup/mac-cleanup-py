from .console import args
from .utils import Collector
from .cli import main  # noqa ignore F401

try:
    from .__version__ import __version__
except ImportError:  # pragma: no cover
    __version__ = "source"

__title__ = "mac-cleanup-py"
__all__ = [
    "Collector", "args",
]
