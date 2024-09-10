"""Core for collecting all unit modules."""

from functools import partial
from itertools import chain
from pathlib import Path as Path_
from types import TracebackType
from typing import Any, Final, Optional, Type, TypeGuard, TypeVar, final

import attr
from beartype import beartype  # pyright: ignore [reportUnknownVariableType]

from mac_cleanup.core_modules import BaseModule, Path

T = TypeVar("T")


@final
@attr.s(slots=True)
class Unit:
    """Unit containing message and the modules list."""

    message: str = attr.ib()
    modules: list[BaseModule] = attr.ib(
        factory=list,
        validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(BaseModule),
            iterable_validator=attr.validators.instance_of(list),  # pyright: ignore [reportUnknownArgumentType]
        ),
    )


@final
class _Collector:
    """Class for collecting all modules."""

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

    @property
    def get_temp_message(self) -> Optional[str]:
        """Getter of private potentially empty attr temp_message."""

        return getattr(self, "_Collector__temp_message", None)

    @property
    def get_temp_modules_list(self) -> Optional[list[BaseModule]]:
        """Getter of private potentially empty attr temp_modules_list."""

        return getattr(self, "_Collector__temp_modules_list", None)

    def __enter__(self) -> "_Collector":
        # Set temp stuff
        self.__temp_message = "Working..."
        self.__temp_modules_list = list()

        # Return self
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        # Raise error if once occurred
        if exc_type:
            raise exc_type(exc_value)

        # Add Unit to list if modules list exists
        if self.__temp_modules_list:
            self._execute_list.append(Unit(message=self.__temp_message, modules=self.__temp_modules_list))

        # Unset temp stuff
        del self.__temp_message
        del self.__temp_modules_list

    @beartype
    def message(self, message_: str) -> None:
        """
        Add message to instance of :class:`Unit`

        :param message_: Message to be printed in progress bar
        """

        self.__temp_message = message_

    @beartype
    def add(self, module_: BaseModule) -> None:
        """
        Add module to the list of modules to instance of :class:`Unit`

        :param module_: Module based on
        :class: `BaseModule`
        """

        self.__temp_modules_list.append(module_)

    @staticmethod
    def _get_size(path_: Path_) -> float:
        """
        Counts size of directory.

        :param path_: Path to the directory
        :return: Size of specified directory
        """

        # Get path posix
        path_posix = path_.as_posix()

        # Set list of globs
        globs = ["*", "[", "]"]

        # Set glob list
        glob_constructor: list[str] = list()

        # Check if there is glob in path
        if any(glob in path_posix for glob in globs):
            # Set glob index list
            globs_index_list: list[int] = list()

            # Find glob indexes
            for glob in globs:
                try:
                    globs_index_list.append(path_posix.index(glob))
                except ValueError:
                    continue

            # Find first glob
            first_wildcard_position = min(globs_index_list)

            # Remove glob from path
            path_ = Path_(path_posix[:first_wildcard_position])

            # Update glob
            glob_constructor.append(path_posix[first_wildcard_position:])

            # Set is_file flag to False (globs can't be files)
            is_file = False
        else:
            # Check if path is a file
            is_file = path_.is_file()

        # Return size if path is a file
        if is_file:
            # Except SIP, symlinks, and not non-existent path
            try:
                return path_.stat(follow_symlinks=False).st_size
            except (PermissionError, FileNotFoundError):
                return 0

        # Add recursive glob
        glob_constructor.append("**/*")

        temp_size: float = 0

        glob_list: list[str] = list()

        # Construct glob_list
        if len(glob_constructor) == 1:
            # Add recursive glob on no glob in path
            glob_list.extend(glob_constructor)
        else:
            # Add specified glob
            glob_list.append(glob_constructor[0])
            # Add recursive glob
            glob_list.append("/".join(glob_constructor))

        # Find every file and count size
        for glob in glob_list:
            for file in path_.glob(glob):
                try:
                    temp_size += file.stat(follow_symlinks=False).st_size
                # Except SIP, symlinks, and not non-existent path
                except (PermissionError, FileNotFoundError):
                    continue
        return temp_size

    @staticmethod
    def __filter_modules(module_: BaseModule, filter_type: Type[T]) -> TypeGuard[T]:
        """Filter instances of specified class based on :class:`BaseModule`"""

        return isinstance(module_, filter_type)

    def _count_dry(self) -> float:
        """Counts free space for dry run :return: Approx amount of bytes to be removed."""

        from concurrent.futures import ThreadPoolExecutor, as_completed

        from mac_cleanup.progress import ProgressBar

        # Extract all modules
        all_modules = list(chain.from_iterable([unit.modules for unit in self._execute_list]))

        # Filter modules based on Path
        path_modules: list[Path] = list(filter(partial(self.__filter_modules, filter_type=Path), all_modules))

        # Extracts paths from path_modules list
        path_list: list[Path_] = [path.get_path for path in path_modules]

        # Set counter for estimated size
        estimate_size: float = 0

        # Get thread executor
        executor = ThreadPoolExecutor()

        try:
            # Add tasks to executor
            tasks = [executor.submit(self._get_size, path) for path in path_list]

            # Wait for task completion and add ProgressBar
            for future in ProgressBar.wrap_iter(
                as_completed(tasks), description="Collecting dry run", total=len(path_list)
            ):
                estimate_size += future.result(timeout=10)
        except KeyboardInterrupt:
            # Shutdown executor without waiting for tasks
            executor.shutdown(wait=False)
        else:
            # Cleanup executor
            executor.shutdown(wait=True)
        return estimate_size


class ProxyCollector:
    """Proxy for accessing :class:`Collector` in a context manager."""

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
        traceback: Optional[TracebackType],
    ) -> None:
        return self.__base.__exit__(exc_type, exc_value, traceback)
