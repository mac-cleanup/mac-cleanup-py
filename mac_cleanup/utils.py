from rich.progress import track
from glob import glob
from os.path import expanduser, exists
from subprocess import Popen, PIPE, DEVNULL
from typing import TypeVar, Callable, Type, Optional, Union
from inspect import isclass

home = expanduser("~")


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
    return (
        Popen(command, shell=True, stdout=PIPE, stderr=DEVNULL)
        .communicate()
        [0]
        .strip()
        .decode("utf-8", errors='replace')
    )


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
    if path.startswith("~"):
        path = home + path[1:]
    return exists(path)


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
        f"{home}/Documents",
        f"{home}/Downloads",
        f"{home}/Desktop",
        f"{home}/Movies",
        f"{home}/Music",
        f"{home}/Pictures",
    ]
    if (
            any([path.startswith(i) for i in SIP_list + user_list])
            or not check_exists(path)
    ):
        return False
    restricted = (
            "restricted" not in cmd(f'ls -lo "{path}"')
            and not bool(cmd(f'xattr -l "{path}"'))  # Returns None if not restricted otherwise string
    )
    return restricted


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
    from os import walk
    from os.path import join, getsize

    total_size = 0
    for dir_path, dir_names, filenames in walk(path):
        for filename in filenames:
            tmp_size = getsize(join(dir_path, filename))
            total_size += tmp_size
    return total_size


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


class CleanUp:
    execute_list: list[dict] = list()

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
        query_list = (
            self.execute_list[-1].setdefault("query", list())
            if not dry
            else self.execute_list[-1].setdefault("dry", list())
        )

        if query.startswith('~'):
            query_list.extend(
                [path for path in glob(home + query[1:]) if check_deletable(path)]
            )
        else:
            if command:
                query_list.extend(
                    ["cmd_" + query]
                )
            else:
                query_list.extend(
                    [path for path in glob(query) if check_deletable(path)]
                )

    def count_dry(
            self,
    ) -> int:
        """
        Counts free space for dry dun

        Returns:
            Approx amount of bytes to be removed
        """
        path_list = list()

        for tasks in self.execute_list:
            path_list.extend(
                [task for task in tasks["query"] if not task.startswith("cmd_")]
            )

            path_list.extend(
                [task for task in tasks.get("dry", "") if not task.startswith("cmd_")]
            )

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
            self.exception = KeyboardInterrupt

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
            except BaseException as caughtException:
                from mac_cleanup.console import console

                if not type(caughtException) in self.exception:
                    import traceback

                    console.print(f"Error occurred - {caughtException}")
                    console.print(traceback.format_exc())
                console.print("\nExiting...")

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
