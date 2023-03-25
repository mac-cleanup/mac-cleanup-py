try:  # For gh-actions
    from importlib.metadata import version

    __version__ = version(__package__)
except ModuleNotFoundError:
    __version__ = "source"
