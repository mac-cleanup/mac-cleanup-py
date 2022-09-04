try:  # For gh-actions
    from importlib.metadata import version

    __version__ = version(__package__)
except ModuleNotFoundError:  # pragma: no cover
    __version__ = "source"
