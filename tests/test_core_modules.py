"""All tests for mac_clean_up.config"""
import pytest

from mac_cleanup.progress import ProgressBar
from mac_cleanup.utils import cmd, check_deletable, check_exists
from mac_cleanup.core_modules import BaseModule, Command, Path, _BaseCommand  # noqa


class TestBaseModule:
    @pytest.mark.parametrize
    def test_with_prompt(self):
        base_module = BaseModule()
        assert base_module.with_prompt() == base_module
        assert base_module.with_prompt("Custom message") == base_module

    def test_execute(self):
        with pytest.raises(NotImplementedError):
            base_module = BaseModule()
            base_module._execute()


class TestBaseCommand:
    def test_init(self, monkeypatch):
        monkeypatch.setattr(cmd, "sudo -E whoami", "root")
        base_command = _BaseCommand(command_="echo 'test'")
        assert base_command is not None

    def test_execute(self, monkeypatch):
        monkeypatch.setattr(cmd, "sudo -E whoami", "root")
        monkeypatch.setattr(ProgressBar, "prompt", lambda *_: True)

        base_command = _BaseCommand(command_="echo 'test'")
        result = base_command._execute()
        assert result is None

class TestCommand:
    def test_with_errors(self):
        command = Command("echo 'test'")
        assert command.with_errors() == command

    def test_execute(self, monkeypatch):
        monkeypatch.setattr(cmd, "sudo -E whoami", "root")
        monkeypatch.setattr(ProgressBar, "prompt", lambda *_: True)

        command = Command("echo 'test'")
        result = command._execute()
        assert result == "test"

class TestPath:
    def test_init(self):
        path = Path("~/test_folder")
        assert path.get_path.as_posix() == "~/test_folder"

    def test_dry_run_only(self):
        path = Path("~/test_folder")
        assert path.dry_run_only() == path

    def test_execute(self, monkeypatch):
        monkeypatch.setattr(cmd, "sudo -E whoami", "root")
        monkeypatch.setattr(ProgressBar, "prompt", lambda *_: True)
        monkeypatch.setattr(check_deletable, "path", lambda *_: True)
        monkeypatch.setattr(check_exists, "path", lambda *_: False)

        path = Path("~/test_folder")
        path.dry_run_only()
        result = path._execute()
        assert result is None

        path_not_dry_run = Path("~/test_folder")
        result_not_dry_run = path_not_dry_run._execute()
        assert result_not_dry_run is None

    def test_execute_not_deletable(self, monkeypatch):
        monkeypatch.setattr(cmd, "sudo -E whoami", "root")
        monkeypatch.setattr(ProgressBar, "prompt", lambda *_: True)
        monkeypatch.setattr(check_deletable, "path", lambda *_: False)
        monkeypatch.setattr(check_exists, "path", lambda *_: True)

        path = Path("~/test_folder")
        result = path._execute()
        assert result is None
