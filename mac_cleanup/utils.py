from pathlib import Path
from typing import Optional, cast

from beartype import beartype  # pyright: ignore [reportUnknownVariableType]
from xattr import xattr  # pyright: ignore [reportMissingTypeStubs]


@beartype
def cmd(command: str, *, ignore_errors: bool = True) -> str:
    """
    Executes command in Popen.

    :param command: Bash command
    :param ignore_errors: If True, no stderr in return
    :return: stdout of executed command
    """

    from subprocess import DEVNULL, PIPE, Popen

    # Get stdout and stderr from PIPE
    out_tuple = Popen(command, shell=True, stdout=PIPE, stderr=(DEVNULL if ignore_errors else PIPE)).communicate()

    # Cast correct type on out_tuple
    out_tuple = cast(tuple[Optional[bytes], Optional[bytes]], out_tuple)

    # Filter NoneType output and decode it
    filtered_out = [out.decode("utf-8", errors="replace").strip() for out in out_tuple if out is not None]

    return "".join(filtered_out)


@beartype
def expanduser(str_path: str) -> str:
    """
    Expands user.

    :param str_path: Path to be expanded
    :return: Path with extended user path as a posix
    """

    from pathlib import Path

    return Path(str_path).expanduser().as_posix()


@beartype
def check_exists(path: Path | str, *, expand_user: bool = True) -> bool:
    """
    Checks if path exists.

    :param path: Path to be checked
    :param expand_user: True if path needs to be expanded
    :return: True if specified path exists
    """

    if not isinstance(path, Path):
        path = Path(path)

    if expand_user:
        path = path.expanduser()

    # If glob return True (it'll delete nothing at the end, hard to hande otherwise)
    if "*" in path.as_posix():
        return True

    return path.exists()


@beartype
def check_deletable(path: Path | str) -> bool:
    """
    Checks if path is deletable.

    :param path: Path to be deleted
    :return: True if specified path is deletable
    """

    # Convert path to correct type
    if not isinstance(path, Path):
        path_: Path = Path(path)
    else:
        path_ = path

    sip_list = ["/System", "/usr", "/sbin", "/Applications", "/Library", "/usr/local"]

    user_list = ["~/Documents", "~/Downloads", "~/Desktop", "~/Movies", "~/Pictures"]

    # Returns False if empty
    if (path_posix := path_.as_posix()) == ".":
        return False

    # If glob return True (it'll delete nothing at the end, hard to hande otherwise)
    if "*" in path_posix:
        return True

    # Returns False if path startswith anything from SIP list or in custom list
    if any(path_posix.startswith(protected_path) for protected_path in list(map(expanduser, sip_list + user_list))):
        return False

    return "com.apple.rootless" not in xattr(path_posix)


@beartype
def bytes_to_human(size_bytes: int | float) -> str:
    """
    Converts bytes to human-readable format.

    :param size_bytes: Bytes
    :return: Human readable size
    """

    from math import floor, log, pow

    if size_bytes <= 0:
        return "0B"

    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(floor(log(size_bytes, 1024)))
    p = pow(1024, i)
    s = round(size_bytes / p, 2)

    return f"{s} {size_name[i]}"
