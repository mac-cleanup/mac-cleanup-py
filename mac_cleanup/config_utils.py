from typing import Optional, Callable

from inspect import getmembers, isfunction

# TODO: check everything
def load_default() -> dict[str, Callable]:
    """
    Load the default modules
        :return: Dict w/ the module name and the module function respectively
    """

    from mac_cleanup import default_modules

    # getmembers returns sorted set
    return dict(getmembers(default_modules, isfunction))


def load_custom(
        custom_path: Optional[str]
) -> dict[str, Callable]:
    """
    Load the custom modules
        :param custom_path: Path to the custom module directory
        :return: Dict w/ the module name and the module function respectively
    """

    if not custom_path:
        return dict()

    from importlib.machinery import SourceFileLoader
    from pathlib import Path

    custom_modules: dict[str, Callable] = dict()

    # Imports all modules from the given path
    for module in Path(custom_path).expanduser().rglob("*.py"):
        # Duplicates will be overwritten
        custom_modules.update(
            dict(
                getmembers(
                    SourceFileLoader(
                        module.name.split(".py")[0],
                        module.as_posix(),
                    ).load_module(),
                    isfunction,
                )
            )
        )

    # getmembers returns sorted dict
    return custom_modules
