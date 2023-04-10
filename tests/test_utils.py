"""All tests for mac_cleanup_py.utils"""
from pathlib import Path
from typing import Optional

import pytest
from beartype.roar import BeartypeCallHintParamViolation


@pytest.mark.parametrize(
    ("command", "ignore_errors", "output"),
    [
        # test empty output
        ("echo", True, ""),
        # test stdout
        ("echo 'test'", True, "test"),
        # test no errors
        ("echo 'test' >&2", True, ""),
        # test redirect stderr
        ("echo 'test' >&2", False, "test"),
        # test beartype
        (123, True, ""),
    ],
)
def test_cmd(command: str | int, ignore_errors: bool, output: str):
    """Test :class:`subprocess.Popen` command execution in :meth:`mac_cleanup.utils.cmd`"""

    from mac_cleanup.utils import cmd

    if isinstance(command, int):
        with pytest.raises(BeartypeCallHintParamViolation):
            cmd(command=command, ignore_errors=ignore_errors)  # pyright: ignore [reportGeneralTypeIssues] # noqa
        return

    assert cmd(command=command, ignore_errors=ignore_errors) == output


@pytest.mark.parametrize(
    ("str_path", "output"),
    [
        # test empty
        ("", ""),
        # test expand home
        ("~/", None),
        # test beartype
        (123, None),
    ],
)
def test_expanduser(str_path: str | int, output: Optional[str], get_current_os: str):
    """Test wrapper of :meth:`pathlib.Path.expanduser` in :meth:`mac_cleanup.utils.expanduser`"""

    from mac_cleanup.utils import expanduser

    if isinstance(str_path, int):
        with pytest.raises(BeartypeCallHintParamViolation):
            expanduser(str_path=str_path)  # pyright: ignore [reportGeneralTypeIssues] # noqa
        return

    if output is None:
        assert expanduser(str_path=str_path).startswith("/Users/" if get_current_os == "Darwin" else "/home/runner")
        return

    assert expanduser(str_path=str_path) == "."


@pytest.mark.parametrize(
    ("path", "output", "expand_path"),
    [
        # test existing str path
        ("/", True, True),
        # test expand user
        ("~/Documents", True, True),
        ("~/Documents", False, False),
        # test Glob
        ("*", True, True),
        # test non-existing str path
        ("/aboba", False, True),
        # test existing Path
        (Path("/"), True, True),
        # test expand user Path
        (Path("~/Documents"), True, True),
        (Path("~/Documents"), False, False),
        # test Glob in Path
        (Path("*"), True, True),
        # test non-existing Path
        (Path("/aboba"), False, True),
        # test beartype
        (123, False, True),
    ],
)
def test_check_exists(path: Path | str | int, output: bool, expand_path: bool):
    """Test wrapper of :meth:`pathlib.Path.exists` in :meth:`mac_cleanup.utils.check_exists`"""

    from mac_cleanup.utils import check_exists

    if isinstance(path, int):
        with pytest.raises(BeartypeCallHintParamViolation):
            check_exists(path=path, expand_user=expand_path)  # pyright: ignore [reportGeneralTypeIssues] # noqa
        return

    assert check_exists(path=path, expand_user=expand_path) is output


@pytest.mark.parametrize(
    ("path", "output"),
    [
        # test deletable str path
        ("/", True),
        # test empty str path
        ("", False),
        # test Glob in str path
        ("*", True),
        # test deletable Path
        (Path("/"), True),
        # test empty Path
        (Path(""), False),
        # test Glob in Path
        (Path("*"), True),
        # test SIP
        ("/System", False),
        (Path("/System"), False),
        # test no expand user
        ("~/Documents", True),
        (Path("~/Documents").expanduser(), False),
        # test custom rules
        (Path("~/Documents"), True),
        # test beartype
        (123, False),
    ],
)
def test_check_deletable(path: Path | str | int, output: bool):
    """Test :meth:`mac_cleanup.utils.check_deletable` with SIP and custom restriction list"""

    from mac_cleanup.utils import check_deletable

    if isinstance(path, int):
        with pytest.raises(BeartypeCallHintParamViolation):
            check_deletable(path=path)  # pyright: ignore [reportGeneralTypeIssues] # noqa
        return

    assert check_deletable(path=path) is output


@pytest.mark.parametrize(
    ("byte", "in_power", "output"),
    [
        # test empty
        (0, 1, "0B"),
        # test B
        (0, 0, "1.0 B"),
        # test KB
        (1024, 1, "1.0 KB"),
        # test MB
        (1024, 2, "1.0 MB"),
        # test GB
        (1024, 3, "1.0 GB"),
        # test TB
        (1024, 4, "1.0 TB"),
        # test beartype
        ("", 0, ""),
    ],
)
def test_bytes_to_human(byte: int | str, in_power: int, output: str):
    """Test bytes to human conversion in :meth:`mac_cleanup.utils.bytes_to_human`"""

    from mac_cleanup.utils import bytes_to_human

    if isinstance(byte, str):
        with pytest.raises(BeartypeCallHintParamViolation):
            bytes_to_human(size_bytes=byte)  # pyright: ignore [reportGeneralTypeIssues] # noqa
        return

    assert bytes_to_human(size_bytes=byte**in_power) == output
