"""Test main script in mac_cleanup_py.main"""
from pathlib import Path as Pathlib
from typing import Any, Callable

import pytest
from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from mac_cleanup import Command, Path, main
from mac_cleanup.config import Config
from mac_cleanup.core import Unit
from mac_cleanup.core_modules import BaseModule
from mac_cleanup.main import EntryPoint


class TestEntryPoint:
    def test_count_free_space(self):
        """Test :meth:`mac_cleanup.main.EntryPoint.count_free_space`"""

        # Get current free space
        res = EntryPoint.count_free_space()

        # Check result is float
        assert isinstance(res, float)

        # Check result is not empty
        assert res > 0

    def test_custom_path_set_prompt(self, monkeypatch: MonkeyPatch):
        """Test configuration for custom path prompted in :class:`mac_cleanup.main.EntryPoint`"""

        # Dummy custom path setter raising SystemExit
        dummy_set_custom_path: Callable[[Config], None] = lambda cfg_self: exit(0)

        # Simulate custom path prompted
        monkeypatch.setattr("mac_cleanup.parser.Args.custom_path", True)

        # Simulate custom path setter
        monkeypatch.setattr("mac_cleanup.config.Config.set_custom_path", dummy_set_custom_path)

        # Check custom path setter being called
        with pytest.raises(SystemExit):
            main()

    @pytest.mark.parametrize("size_multiplier", [3.0, 2.0])
    def test_cleanup(
        self,
        size_multiplier: float,
        path_with_root: None,
        command_with_root: None,
        capsys: CaptureFixture[str],
        monkeypatch: MonkeyPatch,
    ):
        """Test cleanup in :class:`mac_cleanup.main.EntryPoint`"""

        # Dummy Config with empty init
        def dummy_config_init(cfg_self: Config, config_path_: Pathlib) -> None:  # noqa  # noqa
            return

        # Dummy Config with empty call
        def dummy_config_call(config_path_: Pathlib, configuration_prompted: bool) -> None:  # noqa  # noqa
            return

        # Dummy count_free_space for simulating cleaned half of free space
        def dummy_count_free_space(entry_self: EntryPoint) -> float:  # noqa
            if not hasattr(dummy_count_free_space, "called"):
                dummy_count_free_space.called = True  # pyright: ignore [reportFunctionMemberAccess]

                return 1024**2 * size_multiplier / 2
            else:
                return 1024**2 * size_multiplier

        # Dummy module execution (empty one)
        dummy_module_execute: Callable[[BaseModule], None] = lambda md_self: None

        # Simulate Command/Path execution
        monkeypatch.setattr("mac_cleanup.core_modules.Command._execute", dummy_module_execute)
        monkeypatch.setattr("mac_cleanup.core_modules.Path._execute", dummy_module_execute)

        # Simulate Config with empty one
        monkeypatch.setattr("mac_cleanup.config.Config.__init__", dummy_config_init)
        monkeypatch.setattr("mac_cleanup.config.Config.__call__", dummy_config_call)

        # Simulate count_free_space results
        monkeypatch.setattr(EntryPoint, "count_free_space", dummy_count_free_space)

        # Dummy execution list
        dummy_execute_list: list[Unit] = [
            Unit(message="test_1", modules=[Path("test"), Command("test")]),
            Unit(message="test_2", modules=[Path("test")]),
            Unit(message="test_3", modules=[Command("test")]),
        ]

        # Simulate execution list in BaseCollector
        monkeypatch.setattr(EntryPoint.base_collector, "_execute_list", dummy_execute_list)

        # Call entrypoint
        main()

        # Get stdout
        captured_stdout = capsys.readouterr().out

        # Check status in title
        assert "Success" in captured_stdout

        # Check correct size in stdout
        assert f"Removed - {size_multiplier / 2} GB" in captured_stdout

    @pytest.mark.parametrize("cleanup_prompted", [True, False])
    def test_dry_run_prompt(self, cleanup_prompted: bool, capsys: CaptureFixture[str], monkeypatch: MonkeyPatch):
        """Test dry_run with optional cleanup in :class:`mac_cleanup.main.EntryPoint`"""

        # Dummy count_dry returning 1 GB
        dummy_count_dry: Callable[..., float] = lambda: float(1024**3)

        # Dummy Config with empty init
        def dummy_config_init(cfg_self: Config, config_path_: Pathlib) -> None:  # noqa  # noqa
            return

        # Dummy Config with empty call
        def dummy_config_call(config_path_: Pathlib, configuration_prompted: bool) -> None:  # noqa  # noqa
            return

        # Dummy user input in prompt for optional cleanup
        dummy_input: Callable[..., str] = lambda *_, **__: "y" if cleanup_prompted else "n"

        # Dummy cleanup (empty one)
        dummy_cleanup: Callable[[EntryPoint], None] = lambda entry_self: None

        # Simulate user input in prompt for optional cleanup
        monkeypatch.setattr("rich.prompt.PromptBase.get_input", dummy_input)

        # Simulate Config with empty one
        monkeypatch.setattr("mac_cleanup.config.Config.__init__", dummy_config_init)
        monkeypatch.setattr("mac_cleanup.config.Config.__call__", dummy_config_call)

        # Simulate count_dry with predefined result
        monkeypatch.setattr(EntryPoint.base_collector, "_count_dry", dummy_count_dry)

        # Simulate empty cleanup
        monkeypatch.setattr(EntryPoint, "cleanup", dummy_cleanup)

        # Simulate dry run was prompted
        monkeypatch.setattr("mac_cleanup.parser.Args.dry_run", True)

        # Call entrypoint
        main()

        # Get stdout
        captured_stdout = capsys.readouterr().out

        # Check title and body with estimated size
        assert "Dry run results" in captured_stdout
        assert "Approx 1.0 GB will be cleaned" in captured_stdout

        # Check exit message
        if not cleanup_prompted:
            assert "Exiting..." in captured_stdout

    def test_test_dry_run_prompt_error(self, capsys: CaptureFixture[str], monkeypatch: MonkeyPatch):
        """Test errors in dry_run in :class:`mac_cleanup.main.EntryPoint`"""

        # Dummy count_dry returning 1 GB
        dummy_count_dry: Callable[..., float] = lambda: float(1024**3)

        # Dummy Config with no init and empty call
        # Dummy Config with empty init
        def dummy_config_init(cfg_self: Config, config_path_: Pathlib) -> None:  # noqa  # noqa
            return

        # Dummy Config with empty call
        def dummy_config_call(config_path_: Pathlib, configuration_prompted: bool) -> None:  # noqa  # noqa
            return

        # Dummy user input in prompt raising random decode error
        def dummy_input(*args: Any, **kwargs: Any) -> None:  # noqa
            raise UnicodeDecodeError("test", bytes(), 0, 1, "test")

        # Simulate user input in prompt with decode error
        monkeypatch.setattr("rich.prompt.PromptBase.get_input", dummy_input)

        # Simulate Config with empty one
        monkeypatch.setattr("mac_cleanup.config.Config.__init__", dummy_config_init)
        monkeypatch.setattr("mac_cleanup.config.Config.__call__", dummy_config_call)

        # Simulate count_dry with predefined result
        monkeypatch.setattr(EntryPoint.base_collector, "_count_dry", dummy_count_dry)

        # Simulate dry run was prompted
        monkeypatch.setattr("mac_cleanup.parser.Args.dry_run", True)

        # Call entrypoint
        main()

        # Get stdout
        captured_stdout = capsys.readouterr().out

        # Check title and body with estimated size
        assert "Dry run results" in captured_stdout
        assert "Approx 1.0 GB will be cleaned" in captured_stdout

        # Check error message and exit message
        assert "Do not enter symbols that can't be decoded to UTF-8" in captured_stdout
        assert "Exiting..." in captured_stdout
