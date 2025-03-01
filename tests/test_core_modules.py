"""All tests for mac_cleanup_py.config."""

import tempfile
from pathlib import Path as Pathlib
from typing import IO, Callable, Optional, cast

import pytest
from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from mac_cleanup import args
from mac_cleanup.core_modules import Command, Path


class TestCommand:
    @pytest.mark.parametrize(
        ("prompt_succeeded", "prompt", "force_flag"),
        [
            (True, "prompt", False),
            (True, "prompt", True),
            (True, None, False),
            (True, None, True),
            (False, "prompt", False),
            (False, "prompt", True),
            (False, None, False),
            (False, None, True),
        ],
    )
    def test_base_module_execute(
        self,
        prompt_succeeded: bool,
        prompt: Optional[str],
        force_flag: bool,
        capsys: CaptureFixture[str],
        monkeypatch: MonkeyPatch,
    ):
        """Test prompt functionality in :class:`mac_cleanup.core_modules.BaseModule`"""

        args.force = force_flag

        # Dummy user input in prompt
        dummy_input: Callable[..., str] = lambda *_, **__: "" if force_flag else "y" if prompt_succeeded else "n"

        # Simulate user input in prompt
        monkeypatch.setattr("rich.prompt.PromptBase.get_input", dummy_input)

        # Get command with prompt
        command = Command("echo 'test'").with_prompt(message_=prompt)

        # Get command execution output
        captured_execute = command._execute()

        # Check command execution based on prompt success
        if prompt_succeeded or force_flag:
            assert captured_execute is not None
            assert "test" in captured_execute
        else:
            assert captured_execute is None

        if force_flag:
            return

        # Get stdout
        captured_stdout = capsys.readouterr().out

        # Change prompt message to default message if prompt was empty
        if prompt is None:
            prompt = "Do you want to proceed?"

        # Check prompt text
        assert prompt in captured_stdout

        # Check prompt title
        assert "Module requires attention" in captured_stdout

    @pytest.mark.parametrize(
        "executed_command",
        # Empty command or None
        ["", None],
    )
    def test_base_command_execute(self, executed_command: Optional[str]):
        """Test no command being passed to :class:`mac_cleanup.core_modules._BaseCommand`"""

        # Get command instance without command
        command = Command(executed_command)

        # Get stdout
        captured_stdout = command._execute()

        # Check there is no output and no errors
        assert captured_stdout is None

    @pytest.mark.parametrize("redirect_errors", [True, False])
    def test_with_errors(self, redirect_errors: bool):
        # Get command with stderr
        command = Command("echo 'test' >&2")

        # Specify redirecting errors in Command instance
        if redirect_errors:
            command = command.with_errors()

        # Get command execution output
        captured_execute = command._execute()

        # Check command execution output is not empty
        assert captured_execute is not None

        # Check if stderr was captured
        if redirect_errors:
            assert "test" in captured_execute
            return

        # Check if stderr wasn't captured
        assert "test" not in captured_execute


class TestPath:
    @pytest.mark.parametrize("is_file", [True, False])
    def test_init(self, is_file: bool):
        """Tests path and command in init of :class:`mac_cleanup.core_modules.Path`"""

        # Get tmp file
        if is_file:
            tmp_file_object = tempfile.NamedTemporaryFile(mode="w+", delete=False)  # noqa: SIM115
        else:
            tmp_file_object = tempfile.TemporaryDirectory()

        with tmp_file_object as f:
            # Get name from file
            if is_file:
                f = cast(IO[str], f)
                f_name: str = f.name
            else:
                f = cast(str, f)
                f_name: str = f

            # Get tmp path posix
            tmp_path_posix = Pathlib(f_name).as_posix()

            # Get Path instance
            path = Path(tmp_path_posix)

            # Check path
            assert path.get_path.as_posix() == tmp_path_posix

            # Check command
            assert path.get_command == f"rm -rf '{tmp_path_posix}'"  # noqa

    def test_init_expanduser(self):
        """Test expand user in :class:`mac_cleanup.core_modules.Path`"""

        # Get dummy path posix
        tmp_path_posix = Pathlib("~/test")

        # Get Path instance
        path = Path(tmp_path_posix.as_posix())

        # Check path
        assert path.get_path.as_posix() == tmp_path_posix.expanduser().as_posix()

        # Check command
        assert path.get_command == f"rm -rf '{tmp_path_posix.expanduser().as_posix()}'"  # noqa

    @pytest.mark.parametrize("is_file", [True, False])
    def test_dry_run_only(self, is_file: bool):
        """Test dry run only in :class:`mac_cleanup.core_modules.Path`"""

        # Get tmp file
        if is_file:
            tmp_file_object = tempfile.NamedTemporaryFile(mode="w+", delete=False)  # noqa: SIM115
        else:
            tmp_file_object = tempfile.TemporaryDirectory()

        with tmp_file_object as f:
            # Get name from file
            if is_file:
                f = cast(IO[str], f)
                f_name: str = f.name
            else:
                f = cast(str, f)
                f_name: str = f

            # Get tmp path
            tmp_path = Pathlib(f_name)

            # Get Path instance with flag dry_run_only
            path = Path(tmp_path.as_posix()).dry_run_only()

            # Invoke path deletion
            path._execute()

            # Check path exists
            assert tmp_path.exists()

    @pytest.mark.parametrize("is_file", [True, False])
    def test_execute(self, is_file: bool):
        """Test for path/dir deletion in :class:`mac_cleanup.core_modules.Path`"""

        # Get tmp file
        if is_file:
            tmp_file_object = tempfile.NamedTemporaryFile(mode="w+", delete=False)  # noqa: SIM115
        else:
            tmp_file_object = tempfile.TemporaryDirectory()

        with tmp_file_object as f:
            # Get name from file
            if is_file:
                f = cast(IO[str], f)
                f_name: str = f.name
            else:
                f = cast(str, f)
                f_name: str = f

            # Get tmp path
            tmp_path = Pathlib(f_name)

            # Get Path instance
            path = Path(tmp_path.as_posix())

            # Invoke path deletion
            path._execute()

            try:
                # Check file doesn't exist
                assert not tmp_path.exists()
            except AssertionError as err:
                # Remove temp file on error
                if is_file:
                    from os import unlink

                    unlink(f_name)

                # Raise error that file exists
                raise FileExistsError from err

    @pytest.mark.parametrize(("deletable", "exist"), [(False, True), (True, False), (False, False)])
    def test_negative_execute(self, deletable: bool, exist: bool, monkeypatch: MonkeyPatch):
        """Test for negative execution in :class:`mac_cleanup.core_modules.Path`"""

        # Dummy check_deletable utility
        dummy_deletable: Callable[[Pathlib | str], bool] = lambda path: deletable

        # Dummy check_exists utility
        dummy_exists: Callable[[Pathlib | str, bool], bool] = lambda path, expand_user: exist

        # Get tmp file
        with tempfile.NamedTemporaryFile(mode="w+") as f:
            # Get tmp path
            tmp_path = Pathlib(f.name)

            # Simulate check_deletable results
            monkeypatch.setattr("mac_cleanup.core_modules.check_deletable", dummy_deletable)

            # Simulate check_exists results
            monkeypatch.setattr("mac_cleanup.core_modules.check_exists", dummy_exists)

            # Invoke Path instance
            Path(tmp_path.as_posix())._execute()

            # Check file exists
            assert tmp_path.exists()
