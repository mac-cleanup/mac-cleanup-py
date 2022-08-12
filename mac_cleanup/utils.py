from typing import TypeVar, Callable, Type, Optional, Union
from inspect import isclass

_function = TypeVar(
    "_function",
    bound=Callable[..., object]
)

_exception = TypeVar(
    "_exception",
    bound=Union[
        Type[BaseException],
        tuple[Type[BaseException]],
        list[Type[BaseException]]
    ])


class ExceptionDecorator:
    """
    Decorator for catching exceptions and printing logs
    """
    exception: _exception

    def __init__(
            self,
            exception: _exception = None,
    ):
        # Sets default exception if none was provided
        if not exception:
            self.exception = tuple()

        # If class convert to tuple
        if isclass(self.exception):
            self.exception = self.exception,

    def __call__(
            self,
            func: _function,
    ):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                from mac_cleanup.console import console

                console.print("\n[warning]Exiting...")
                exit(0)
            # Ignore SystemExit
            except SystemExit:
                pass
            except BaseException as caughtException:
                from mac_cleanup.console import console

                # If not default exception logs stuff in console
                if not type(caughtException) in self.exception:
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
                    os._exit(1)  # noqa  It exists, exit whole process
        return wrapper


def catch_exception(
        func: Optional[_function] = None,
        exception: Optional[_exception] = None,
) -> Union[ExceptionDecorator, _function]:
    """
    Decorator for catching exceptions and printing logs

    Args:
        func: Function to be decorated
        exception: Expected exception(s)
    Returns:
        Decorated function
    """
    exceptor = ExceptionDecorator(exception)
    if func:
        exceptor = exceptor(func)
    return exceptor


def cmd(
        command: str,
) -> str:
    """
    Executes command in Popen

    Args:
        command: Bash command
    Returns:
        stdout of executed command
    """
    from subprocess import Popen, PIPE, DEVNULL

    return (
        Popen(command, shell=True, stdout=PIPE, stderr=DEVNULL)
        .communicate()
        [0]
        .strip()
        .decode("utf-8", errors="replace")
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

    # restricted = (
    #         "restricted" not in cmd(f"ls -lo {path} | awk '{{print $3, $4}}'")
    #         and not bool(cmd(f"xattr -l {path}"))  # Returns None if not restricted otherwise string
    # )
    # return restricted


def get_size(
        path: str,
) -> int:
    """
    Counts size of dir/file

    Args:
        path: Full path to the dir/file
    Returns:
        Size of dir/file
    """
    from pathlib import Path

    # Searching for glob in path
    split_path = path.split("*", 1)
    path, glob = split_path if len(split_path) == 2 else (path, "")

    # Return 0 if SIP check failed
    try:
        return sum(
            p.stat().st_size
            for p in Path(path).expanduser().rglob("*" + glob)
            # Ignores symbolic links
            if not p.is_symlink()
        )
    except PermissionError:
        return 0


def bytes_to_human(
        size_bytes: int,
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


class Borg:
    _shared_state: dict[str, list] = dict()

    def __init__(self):
        self.__dict__ = self._shared_state


class CleanUp(Borg):
    def __init__(self, execute_list=None):
        super().__init__()
        if execute_list:
            self.execute_list = execute_list
        else:
            # initiate the first instance with default state
            if not hasattr(self, "execute_list"):
                self.execute_list: list[dict] = list()

    def msg(
            self,
            message: str,
    ) -> None:
        """
        Creates new dict in execute_list and adds message

        Args:
            message: message to be displayed in progress bar
        """
        self.execute_list.append({"msg": message})

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

        query_list = self.execute_list[-1].setdefault("exec_list", list())

        temp_query = dict()

        # Sets query type
        temp_query["type"] = "dry" if dry else "cmd" if command else "path"

        # Adds query to query_list if deletable and exists
        temp_query["main"] = (
            query
            if temp_query["type"] != "cmd"
            and check_deletable(query)
            and check_exists(query)
            else query
            if temp_query["type"] == "cmd"
            else None
        )

        # Do nothing if main is empty
        if temp_query["main"]:
            query_list.append(temp_query)

    def count_dry(
            self,
    ) -> int:
        """
        Counts free space for dry dun

        Returns:
            Approx amount of bytes to be removed
        """
        from rich.progress import track

        # Extracts paths from execute_list
        path_list = [
            task["main"]
            for tasks in self.execute_list
            for task in tasks["exec_list"]
            if task["type"] != "cmd"
        ]

        counted_list = [
            get_size(path)
            for path in track(
                path_list,
                description="Collecting dry run",
                transient=True,
                total=len(path_list),
            )
        ]

        return sum(counted_list)
