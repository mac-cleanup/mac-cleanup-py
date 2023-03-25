"""Core for collecting all unit modules"""
from typing import final, Final, TypeVar, TypeGuard, Type, Optional, Any
from types import TracebackType

from beartype import beartype  # pyright: ignore [reportUnknownVariableType]

from itertools import chain
from functools import partial

import attr
from pathlib import Path as Path_

from mac_cleanup.core_modules import BaseModule, Path
from mac_cleanup.utils import _KeyboardInterrupt


T = TypeVar("T")


@final
@attr.s(slots=True)
class Unit:
    """Unit containing message and the modules list"""

    message: str = attr.ib()
    modules: list[BaseModule] = attr.ib(
        factory=list,
        validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(BaseModule),
            iterable_validator=attr.validators.instance_of(list)  # pyright: ignore [reportUnknownArgumentType]
        )
    )


@final
class _Collector:
    """Class for collecting all modules"""

    _shared_instance: dict[str, Any] = dict()

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
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType]
    ) -> None:
        # Raise error if once occurred
        if exc_type:
            raise exc_type(exc_value)

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

    @beartype
    def message(
            self,
            message_: str
    ) -> None:
        """
        Add message to instance of :class:`Unit`
            :param message_: Message to be printed in progress bar
        """

        self.__temp_message = message_

    @beartype
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
    def _get_size(
            path_: Path_
    ) -> float:
        """
        Counts size of directory
            :param path_: Path to the directory
            :return: Size of specified directory
        """

        path = path_.expanduser().as_posix()

        try:
            # Searching for glob in path
            split_path = path.split("*", 1)
            path, glob = split_path if len(split_path) == 2 else (path, "")

            temp_size: float = 0

            for p in Path_(path).rglob("*" + glob):
                # Except SIP and symlinks
                try:
                    temp_size += p.stat().st_size
                except (PermissionError, FileNotFoundError):
                    continue
            return temp_size
        except KeyboardInterrupt:
            # Needed to handle KeyboardInterrupt in Pool
            raise _KeyboardInterrupt()

    @staticmethod
    def __filter_modules(
            module_: BaseModule,
            filter_type: Type[T]
    ) -> TypeGuard[T]:
        """Filter instances of specified class based on :class:`BaseModule`"""

        return isinstance(module_, filter_type)

    def _count_dry(self) -> float:
        """
        Counts free space for dry run
            :return: Approx amount of bytes to be removed
        """

        from mac_cleanup.progress import ProgressBar
        from multiprocessing import Pool

        # Extract all modules
        all_modules = list(chain(*[unit.modules for unit in self._execute_list]))

        # Filter modules based on Path
        path_modules: list[Path] = list(
            filter(
                partial(self.__filter_modules, filter_type=Path),
                all_modules
            )
        )

        # Extracts paths from path_modules list
        path_list: list[Path_] = list(map(lambda path: path.get_path, path_modules))

        # Set counter for estimated size
        estimate_size: float = 0

        with Pool() as pool:
            try:
                for path_size in ProgressBar.wrap_iter(
                        pool.imap_unordered(
                            func=self._get_size,
                            iterable=path_list
                        ),
                        description="Collecting dry run",
                        total=len(path_list)
                ):
                    estimate_size += path_size
            except _KeyboardInterrupt:
                # Closing pool w/ pool.close() to wait for unfinished tasks
                pool.close()
                # Waits for the worker processes to terminate
                pool.join()
        return estimate_size


class ProxyCollector:
    """Proxy for accessing :class:`Collector` in a context manager"""

    def __init__(self):
        # Build a Collector object
        self.__base = _Collector()

    def __enter__(self) -> _Collector:
        # Return a Collector object
        return self.__base.__enter__()

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType]
    ) -> None:
        # Raise errors if any
        if exc_type:
            raise exc_type(exc_value)

        return self.__base.__exit__(exc_type, exc_value, traceback)
