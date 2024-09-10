try:  # For gh-actions
    from importlib.metadata import version

    __version__ = version(__package__)  # pyright: ignore [reportArgumentType]
except ModuleNotFoundError:  # pragma: no cover
    __version__ = "source"
