from importlib.metadata import version

try:
    __version__ = version(__package__)
except ModuleNotFoundError:  # For gh-actions  # pragma: no cover
    __version__ = "source"
