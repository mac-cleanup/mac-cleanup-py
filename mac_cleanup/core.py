"""Core for collecting all unit modules"""
from typing import final, Final

from beartype import beartype

from itertools import chain

import attr

from mac_cleanup.core_modules import BaseModule, Path
from mac_cleanup.utils import _KeyboardInterrupt


@final
@attr.s(slots=True)
class Unit:
    """Unit containing message and the modules list"""

    message: str = attr.ib()
    modules: list[BaseModule] = attr.ib(
        factory=list,
        validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(BaseModule),
            iterable_validator=attr.validators.instance_of(list)
        )
    )


@beartype
@final
class _Collector:
    """Class for collecting all modules"""

    _shared_instance = dict()

    # Init temp stuff
    __temp_message: str
    __temp_modules_list: list[BaseModule]

    def __init__(self):
        # Borg implementation
        self.__dict__ = self._shared_instance

        # Add execute_list if none found in shared_instance
        if not hasattr(self, "_execute_list"):
            self._execute_list: Final[list[Unit]] = list()

    def __enter__(self) -> '_Collector':
        # Set temp stuff
        self.__temp_message = "Working..."
        self.__temp_modules_list = list()

        # Return self
        return self

    def __exit__(
            self,
            exc_type,
            exc_val,
            exc_tb
    ) -> None:
        # Raise error if once occurred
        if exc_type:
            raise exc_type(exc_val)

        # Add Unit to list if modules list exists
        if self.__temp_modules_list:
            self._execute_list.append(
                Unit(
                    message=self.__temp_message,
                    modules=self.__temp_modules_list
                )
            )

        # Unset temp stuff
        del self.__temp_message
        del self.__temp_modules_list

    def message(
            self,
            message_: str
    ) -> None:
        """
        Add message to instance of :class:`Unit`
            :param message_: Message to be printed in progress bar
        """

        self.__temp_message = message_

    def add(
            self,
            module_: BaseModule
    ) -> None:
        """
        Add module to the list of modules to instance of :class:`Unit`
            :param module_: Module based on :class:`BaseModule`
        """

        self.__temp_modules_list.append(module_)

    @staticmethod
    def __get_size(
            path: str
    ) -> float:
        """
        Counts size of directory
            :param path: Path to the directory
            :return: Size of specified directory
        """

        from pathlib import Path

        try:
            # Searching for glob in path
            split_path = path.split("*", 1)
            path, glob = split_path if len(split_path) == 2 else (path, "")

            temp_size: float = 0

            for p in Path(path).expanduser().rglob("*" + glob):
                # Except SIP and symlinks
                try:
                    temp_size += p.stat().st_size
                except (PermissionError, FileNotFoundError):
                    continue
            return temp_size
        except KeyboardInterrupt:
            # Needed to handle KeyboardInterrupt in Pool
            raise _KeyboardInterrupt

    @staticmethod
    def __filter_path_modules(
            module_
    ) -> bool:
        """Filter instances of :class:`Path`"""

        return isinstance(module_, Path)

    def _count_dry(self) -> float:
        """
        Counts free space for dry run
            :return: Approx amount of bytes to be removed
        """

        from mac_cleanup.progress import ProgressBar
        from multiprocessing import Pool

        # Extracts paths from execute_list
        modules_list = list(chain(*[unit.modules for unit in self._execute_list]))
        path_modules_list: list[Path] = list(filter(self.__filter_path_modules, modules_list))
        path_list: list[str] = list(map(lambda path: path.__path, path_modules_list))

        module_size: float = 0

        with Pool() as pool:
            try:
                for path_size in ProgressBar.wrap_iter(
                        pool.imap_unordered(
                            self.__get_size,
                            path_list,
                        ),
                        description="Collecting dry run",
                        total=len(path_list),
                ):
                    module_size += path_size
            except _KeyboardInterrupt:  # pragma: no cover
                # Closing pool w/ pool.close() to wait for unfinished tasks
                pool.close()
                # Waits for the worker processes to terminate
                pool.join()
        return module_size


class ProxyCollector:
    """Proxy for accessing :class:`Collector` in a context manager"""

    def __init__(self):
        # Build a Collector object
        self.__base = _Collector()

    def __enter__(self) -> _Collector:
        # Return a Collector object
        return self.__base.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # Raise errors if any
        if exc_type:
            raise exc_type(exc_val)

        return self.__base.__exit__(exc_type, exc_val, exc_tb)
