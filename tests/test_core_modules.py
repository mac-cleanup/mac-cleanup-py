"""All tests for mac_clean_up.config"""
from typing import Optional, Callable

import pytest
from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from mac_cleanup.core_modules import Command


class TestCommand:
    @pytest.mark.parametrize(
        "has_root",
        [False, True]
    )
    def test_base_command_init(
            self,
            has_root: bool,
            capsys: CaptureFixture[str],
            monkeypatch: MonkeyPatch
    ):
        """Test root checking part in init of :class:`mac_cleanup.core_modules._BaseCommand`"""

        # Dummy cmd for checking root
        dummy_cmd: Callable[..., str] = lambda *_, **__: "root" if has_root else ""

        # Simulate root checking
        monkeypatch.setattr("mac_cleanup.core_modules.cmd", dummy_cmd)

        # Raise error if no root
        if not has_root:
            with pytest.raises(AssertionError):
                # root
                Command("echo 'test'")
            return

        # Get Command instance and invoke root checking
        command = Command("echo 'test'")

        # Revert cmd mock
        monkeypatch.undo()

        # Get command execution output
        captured_execute = command._execute()

        # Check command execution output is not empty
        assert captured_execute is not None

        # Check command execution output is correct
        assert "test" in captured_execute

    @pytest.mark.parametrize(
        ("prompt_succeeded", "prompt"),
        [
            (True, "prompt"),
            (True, None),
            (False, "prompt"),
            (False, None)
        ]
    )
    def test_base_module_execute(
            self,
            prompt_succeeded: bool,
            prompt: Optional[str],
            capsys: CaptureFixture[str],
            monkeypatch: MonkeyPatch
    ):
        """Test prompt functionality in :class:`mac_cleanup.core_modules.BaseModule`"""

        # Dummy user input in prompt
        dummy_input: Callable[..., str] = lambda *_, **__: "y" if prompt_succeeded else "n"

        # Simulate user input in prompt
        monkeypatch.setattr("rich.prompt.PromptBase.get_input", dummy_input)

        # Simulate user has root
        monkeypatch.setattr("mac_cleanup.core_modules.Command._BaseCommand__has_root", True)

        # Get command with prompt
        command = Command("echo 'test'").with_prompt(message_=prompt)

        # Get command execution output
        captured_execute = command._execute()

        # Check command execution based on prompt success
        if prompt_succeeded:
            assert captured_execute is not None
            assert "test" in captured_execute
        else:
            assert captured_execute is None

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
        ["", None]
    )
    def test_base_command_execute(
            self,
            executed_command: Optional[str],
            capsys: CaptureFixture[str],
            monkeypatch: MonkeyPatch
    ):
        """Test no command being passed to :class:`mac_cleanup.core_modules._BaseCommand`"""

        # Simulate user has root
        monkeypatch.setattr("mac_cleanup.core_modules.Command._BaseCommand__has_root", True)

        # Get command instance without command
        command = Command(executed_command)

        # Get stdout
        captured_stdout = command._execute()

        # Check there is no output and no errors
        assert captured_stdout is None

    @pytest.mark.parametrize(
        "redirect_errors",
        [True, False]
    )
    def test_with_errors(
            self,
            redirect_errors: bool,
            capsys: CaptureFixture[str],
            monkeypatch: MonkeyPatch
    ):
        # Simulate user has root
        monkeypatch.setattr("mac_cleanup.core_modules.Command._BaseCommand__has_root", True)

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
