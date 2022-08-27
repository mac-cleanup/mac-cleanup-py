import pytest
from mac_cleanup.utils import *


@pytest.mark.parametrize(
    "exception, exit_on_exception, raises",
    [
        # specified exceptions are caught w/o exit
        (
            KeyboardInterrupt,
            False,
            KeyboardInterrupt,
        ),
        # SystemExit caught by default w/o exit
        (
            None,
            True,
            SystemExit,
        ),
        # specified exceptions as a tuple are caught w/o exit
        (
            (ValueError,),
            True,
            ValueError,
        ),
        # Unexpected exception caught w/o exit
        (
            None,
            False,
            ValueError,
        ),
    ]
)
def test_catch_exception(
        exception: Optional[Type[BaseException]],
        exit_on_exception: bool,
        raises: Type[BaseException],
) -> None:
    @catch_exception(
        exception=exception,
        exit_on_exception=exit_on_exception,
    )
    def raise_error() -> None:
        raise raises

    raise_error()


@pytest.mark.parametrize(
    "command, expected, ignore_errors",
    [
        # stdout works
        (
            "echo test",
            "test",
            True,
        ),
        # stderr doesn't work
        (
            "echo test >&2",
            "",
            True,
        ),
        # stderr works w/ ignore_errors agr
        (
            "echo test >&2",
            "test",
            False,
        ),
    ]
)
def test_cmd(
        command: str,
        expected: str,
        ignore_errors: bool,
) -> None:
    assert cmd(
        command=command,
        ignore_errors=ignore_errors
    ) == expected


def test_expand_user(
        get_current_os: str,
) -> None:
    # "~" transforms to user's home location
    assert expanduser("~/").startswith("/Users/" if get_current_os == "Darwin" else "/home/runner")


def test_check_exists(
        get_current_os: str,
) -> None:
    # Always True w/ glob
    assert check_exists("*")
    # Check Users folder exists - always True
    assert check_exists("/Users/" if get_current_os == "Darwin" else "/home/runner")

    from pathlib import Path

    test_folder_path: str = "~/.mac_cleanup"
    test_folder: Path = Path(test_folder_path).expanduser()
    test_folder.mkdir(exist_ok=True)

    test_file: Path = Path(test_folder_path + "/test_dry").expanduser()
    test_file.touch(exist_ok=True)

    results = (
        check_exists("~/.mac_cleanup")
        and check_exists("~/.mac_cleanup/test_dry")
    )

    from os import remove, rmdir

    remove(test_file.as_posix())
    rmdir(test_folder.as_posix())

    assert results


@pytest.mark.parametrize(
    "path, expected",
    [
        # Always False if empty w/ strip
        (" ", False),
        # Always True w/ glob
        ("*", True),
        # Check SIP
        ("/System/test", False),
        # Check user_list
        ("~/Downloads/test", False),
    ]
)
def test_deletable(
        path: str,
        expected: bool,
) -> None:
    assert check_deletable(path) is expected


@pytest.mark.parametrize(
    "byte, human",
    [
        # Check == 0
        (0, "0B"),
        # Check bytes
        (100, "100.0 B"),
        # Check KB
        (1024, "1.0 KB"),
        # Check MB
        (1024 ** 2 * 1.5, "1.5 MB"),
        # Check GB
        (1024 ** 3, "1.0 GB"),
        # Check TB
        (1024 ** 4, "1.0 TB"),
    ]
)
def test_bytes_to_human(
        byte: float,
        human: str,
) -> None:
    assert bytes_to_human(byte) == human


def test_collector_msg() -> None:
    t = Collector(execute_list=list())

    assert t.execute_list == list()
    t.msg("test")
    assert t.execute_list[-1].msg == "test"


def test_collector_sip() -> None:
    t = Collector(execute_list=list())
    t.msg("test")

    t.collect("")
    t.collect("/System/test")
    t.collect("~/Downloads/test")
    assert t.execute_list[-1].unit_list == list()


@pytest.mark.parametrize(
    "query, command, dry",
    [
        # Test command
        ("test", True, False),
        # Test dry
        ("/Users/", False, True),
        # Test path
        ("/Users/", False, False)
    ])
def test_collector_types(
        query: str,
        command: bool,
        dry: bool,
        get_current_os: str,
) -> None:
    t = Collector(execute_list=list())
    t.msg("test")

    if get_current_os != "Darwin":
        query = query.replace("/Users/", "/home/runner/")

    t.collect(query, command=command, dry=dry)
    assert t.execute_list[-1].unit_list[-1].command == query
    assert t.execute_list[-1].unit_list[-1].cmd is command
    assert t.execute_list[-1].unit_list[-1].dry is dry


# Test command & dry
@pytest.mark.xfail(
    raises=ValueError,
)
def test_collector_all_types() -> None:
    t = Collector(execute_list=list())
    t.msg("test")
    t.collect("test", command=True, dry=True)


def test_collector_count_dry() -> None:
    t = Collector(execute_list=list())
    t.msg("test")

    t.collect(
        "echo test",
        command=True,
    )
    assert t.count_dry() == 0

    from pathlib import Path
    from random import random

    test_folder_path: str = "~/.mac_cleanup"
    test_folder: Path = Path(test_folder_path).expanduser()
    test_folder.mkdir(exist_ok=True)

    test_file: Path = Path(test_folder_path + "/test_dry").expanduser()
    test_file.touch(exist_ok=True)

    expected_bytes: int = 1024 ** 2 * 10 * int(random())

    with test_file.open("w") as f:
        f.write("1" * expected_bytes)

    t.collect("~/.mac_cleanup", dry=True)

    actual_bytes = t.count_dry()

    from os import remove, rmdir

    remove(test_file.as_posix())
    rmdir(test_folder.as_posix())

    assert actual_bytes == expected_bytes
