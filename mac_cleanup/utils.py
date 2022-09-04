from __future__ import annotations
from typing import TypeVar, Callable, Type, Optional, Union, overload
from typing import Generic, Tuple, List, Dict  # Generics are fun
from inspect import isclass
from attr import attrs, attrib

function = TypeVar(
    "function",
    bound=Callable[..., object]
)

_exception = TypeVar(
    "_exception",
    # Removed bound 'cause it can only be one type at a time
    Type[BaseException],
    Tuple[Type[BaseException]],
    List[Type[BaseException]],
)


class _ExceptionDecorator(Generic[_exception]):
    """
    Decorator for catching exceptions and printing logs
    """
    exception: Union[_exception, tuple]
    exit_on_exception: bool

    def __init__(
            self,
            exception: Optional[Union[_exception, tuple]] = None,
            exit_on_exception: bool = False,
    ):
        # Sets default exception (empty tuple) if none was provided
        if exception is None:
            self.exception = tuple()
        # Changes exception class to tuple if it's class
        elif isclass(exception):
            self.exception = exception,
        else:
            self.exception = exception
        # Sets exit_on_exception
        self.exit_on_exception = exit_on_exception

    def __call__(  # type: ignore
            self,
            func: function,
    ):
        def wrapper(*args, **kwargs):  # type: ignore
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                from .console import console

                console.print("\n[warning]Exiting...")
                if self.exit_on_exception:
                    exit(0)  # pragma: no cover
            # Ignore SystemExit
            except SystemExit:
                pass
            except BaseException as caughtException:
                from .console import console

                # If not default exception logs stuff in console
                if type(caughtException) not in self.exception:
                    import os
                    from logging import basicConfig, getLogger
                    from rich.logging import RichHandler

                    basicConfig(
                        level="ERROR",
                        format="%(message)s",
                        datefmt="[%X]",
                        handlers=[RichHandler(rich_tracebacks=True)]
                    )

                    log = getLogger("ExceptionDecorator")
                    log.exception("Unexpected error occurred")
                    console.print("\n[danger]Exiting...")
                    if self.exit_on_exception:
                        os._exit(1)  # noqa  It exists, exits whole process  # pragma: no cover

        return wrapper


@overload
def catch_exception(
        func: function,
        exception: Optional[_exception] = ...,
        exit_on_exception: bool = ...,
) -> function:
    ...  # pragma: no cover


@overload
def catch_exception(
        func: None = ...,
        exception: Optional[_exception] = ...,
        exit_on_exception: bool = ...,
) -> _ExceptionDecorator:
    ...  # pragma: no cover


def catch_exception(
        func: Optional[function] = None,
        exception: Optional[_exception] = None,
        exit_on_exception: bool = True,
) -> Union[_ExceptionDecorator, function]:
    """
    Decorator for catching exceptions and printing logs

    Args:
        func: Function to be decorated
        exception: Expected exception(s)
        exit_on_exception: If True, exit after unexpected exception was handled
    Returns:
        Decorated function
    """
    exception_instance = _ExceptionDecorator(
        exception=exception,
        exit_on_exception=exit_on_exception,
    )
    if func:
        exception_instance = exception_instance(func)
    return exception_instance


def cmd(
        command: str,
        ignore_errors: bool = True,
) -> str:
    """
    Executes command in Popen

    Args:
        command: Bash command
        ignore_errors: If True, no stderr in return
    Returns:
        stdout of executed command
    """
    from subprocess import Popen, PIPE, DEVNULL

    return (
        ""
        .join(
            out
            .strip()
            .decode("utf-8", errors="replace")
            for out in Popen(
                command,
                shell=True,
                stdout=PIPE,
                stderr=(DEVNULL if ignore_errors else PIPE),
            )
            .communicate()
            if out is not None
        )
    )


def expanduser(
        str_path: str,
) -> str:
    """
    Expands path (replaces "~" with absolute path)

    Args:
        str_path: Path to be expanded
    Returns:
        Path as a string
    """
    from pathlib import Path

    return Path(str_path).expanduser().as_posix()


def check_exists(
        path: str,
) -> bool:
    """
    Checks if dir/file exists

    Args:
        path: dir/file full path
    Returns:
        True if exists
    """
    from pathlib import Path

    # If glob return True (it'll delete nothing at the end, hard to hande otherwise)
    if "*" in path:
        return True
    return Path(path).expanduser().exists()


def check_deletable(
        path: str,
) -> bool:
    """
    Checks if path is deletable

    Args:
        path: Path to be deleted
    Returns:
        True if path is deletable
    """
    SIP_list = [
        "/System",
        "/usr",
        "/sbin",
        "/Applications",
        "/Library",
        "/usr/local",
    ]

    user_list = [
        "~/Documents",
        "~/Downloads",
        "~/Desktop",
        "~/Movies",
        "~/Music",
        "~/Pictures",
    ]

    # Returns False if empty
    if not path.strip():
        return False

    # If glob return True (it'll delete nothing at the end, hard to hande otherwise)
    if "*" in path:
        return True

    # Returns False if path startswith anything from SIP_list or in user_list
    if any(
            expanduser(path).startswith(i)
            for i in list(map(expanduser, SIP_list + user_list))
    ):
        return False
    return "restricted" not in cmd(f"ls -lo {path} | awk '{{print $3, $4}}'")


class _KeyboardInterrupt(Exception):
    """
    Inherited from Exception class to handle exceptions in multiprocessing.Pool
    """
    pass


def _get_size(
        path: str,
) -> float:  # pragma: no cover
    """
    Counts size of dir/file

    Args:
        path: Full path to the dir/file
    Returns:
        Size of dir/file
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


def bytes_to_human(
        size_bytes: float,
) -> str:
    """
    Converts bytes to human-readable format

    Args:
        size_bytes: Bytes
    Returns: Human readable size
    """
    from math import floor, log, pow

    if size_bytes <= 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(floor(log(size_bytes, 1024)))
    p = pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


@attrs(slots=True, auto_attribs=True)
class _ExecUnit:
    """
    Unit of the execution list
    """
    command: str
    cmd: bool
    dry: bool


@attrs(slots=True)
class _Module:
    """
    Instance of a module. Contains the message and the execution list
    """
    msg: str = attrib()
    unit_list: List[_ExecUnit] = attrib(
        factory=list,
    )


class _Borg:
    _shared_state: Dict[str, list] = dict()

    def __init__(
            self
    ) -> None:
        self.__dict__ = self._shared_state


class Collector(_Borg):
    """
    Class collection execute list of all active modules
    """

    execute_list: List[_Module]

    def __init__(
            self,
            execute_list: Optional[List[_Module]] = None,
    ) -> None:
        super().__init__()
        if execute_list is not None:
            self.execute_list = execute_list
        else:
            # initiate the first instance with default state
            if not hasattr(self, "execute_list"):
                self.execute_list = list()

    def msg(
            self,
            message: str,
    ) -> None:
        """
        Creates new dict in execute_list and adds message

        Args:
            message: message to be displayed in progress bar
        """
        self.execute_list.append(
            _Module(msg=message),
        )

    def collect(
            self,
            query: str,
            command: bool = False,
            dry: bool = False,
    ) -> None:
        """
        Collects paths and commands to be deleted/executed in the iteration

        Args:
            query: Path to be deleted or command to be executed
            command: True if query is a command
            dry: True if query is for dry run only
        """
        if dry and command:
            raise ValueError("Not supported yet")

        # Gets last module's exec_list
        exec_list = self.execute_list[-1].unit_list

        temp_unit = _ExecUnit(
            # Sets query type
            cmd=command,
            dry=dry,

            # Adds command to temp_unit if deletable and exists
            command=(
                query
                if command
                else query
                if check_deletable(query) and check_exists(query)
                else ""
            )
        )

        # Do nothing if main is empty
        if temp_unit.command:
            exec_list.append(temp_unit)

    def count_dry(
            self,
    ) -> float:
        """
        Counts free space for dry dun

        Returns:
            Approx amount of bytes to be removed
        """
        from rich.progress import track
        from multiprocessing import Pool

        # Extracts paths from execute_list
        path_list = [
            unit.command
            for module in self.execute_list
            for unit in module.unit_list
            if not unit.cmd
        ]

        counted_list: float = 0

        with Pool() as pool:
            try:
                for temp_size in track(
                        pool.imap_unordered(
                            _get_size,  # type: ignore
                            path_list,
                        ),
                        description="Collecting dry run",
                        transient=True,
                        total=len(path_list),
                ):
                    counted_list += temp_size
            except _KeyboardInterrupt:  # pragma: no cover
                # Closing pool w/ .close() to wait for unfinished tasks
                pool.close()
                # Waits for the worker processes to terminate
                pool.join()
        return counted_list
