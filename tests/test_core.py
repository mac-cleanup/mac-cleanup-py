"""All tests for mac_cleanup_py.core."""

import os
import tempfile
from pathlib import Path as Pathlib
from random import choice, randint
from typing import Callable, Optional, Type

import pytest
from _pytest.monkeypatch import MonkeyPatch

from mac_cleanup.core import ProxyCollector as Collector
from mac_cleanup.core import _Collector  # noqa
from mac_cleanup.core import Unit
from mac_cleanup.core_modules import BaseModule, Command, Path


class TestUnit:
    def test_create_unit(self):
        """Check :class:`mac_cleanup.core.Unit` creation."""

        # message, module list, validators
        message = "Test message"

        modules: list[BaseModule] = [choice([Command, Path])("") for _ in range(randint(1, 5))]

        unit = Unit(message=message, modules=modules)

        # Check message
        assert unit.message == message

        # Check modules list
        assert unit.modules == modules

        # Check errors
        with pytest.raises(TypeError):
            Unit(message=message, modules=[123])  # pyright: ignore [reportArgumentType] # noqa

        with pytest.raises(TypeError):
            Unit(message=message, modules=123)  # pyright: ignore [reportArgumentType] # noqa


class TestCollector:
    def test_proxy_collector(self):
        """Test :class:`mac_cleanup.core.Collector` is proxy of
        :class:`mac_cleanup.core._Collector`
        """

        with Collector() as t:
            assert isinstance(t, _Collector)

    @pytest.mark.parametrize("raised_error", [IndexError, KeyError, ValueError])
    def test_errors_on_exit(self, raised_error: Type[BaseException]):
        """Test errors being raised from :class:`mac_cleanup.core._Collector` and it's proxy."""

        with pytest.raises(raised_error), Collector() as _:  # noqa: PT012
            raise raised_error

    @staticmethod
    @pytest.fixture
    def base_collector() -> _Collector:
        """Get main collector instance - :class:`mac_cleanup.core._Collector`"""

        return _Collector()

    @pytest.mark.parametrize("message_text", ["Test message", None])
    def test_message_and_add(self, message_text: Optional[str], base_collector: _Collector):
        """Test messages (or default ones) and modules being added to
        :class:`mac_cleanup.core._Collector`
        """

        # Set modules list
        module_list = [Path(""), Command("")]

        with Collector() as t:
            if message_text:
                # Add message
                t.message(message_text)
            else:
                # Add default message if none was specified
                message_text = "Working..."

            # Add modules from list of modules
            for module in module_list:
                t.add(module)

            # Check temp stuff
            assert t.get_temp_message == message_text
            assert t.get_temp_modules_list == module_list

        # Check temp stuff is gone
        assert not hasattr(base_collector, "_Collector__temp_message")
        assert base_collector.get_temp_message is None

        assert not hasattr(base_collector, "_Collector__temp_modules_list")
        assert base_collector.get_temp_modules_list is None

        # Check message and module list were set and are correct
        assert base_collector._execute_list[-1].message == message_text
        assert base_collector._execute_list[-1].modules == module_list

    def test_add_no_module(self, base_collector: _Collector):
        """Test nothing being added without specifying modules in
        :class:`mac_cleanup.core._Collector`
        """

        with Collector() as t:
            t.message("test_add_no_module")

            # Check temp stuff
            assert t.get_temp_message == "test_add_no_module"
            assert t.get_temp_modules_list is not None
            assert len(t.get_temp_modules_list) == 0

        # Check no module with specified message
        assert not len([unit for unit in base_collector._execute_list if unit.message == "test_add_no_module"])

    @pytest.mark.parametrize("size_multiplier", [0, 1, 1024])
    def test_get_size(self, size_multiplier: int, base_collector: _Collector):
        """Test :meth:`mac_cleanup.core._Collector._get_size` works correctly."""

        # Get size in bytes
        size = 1024 * size_multiplier

        with (
            tempfile.TemporaryDirectory() as dir_name,
            tempfile.NamedTemporaryFile(mode="w+b", dir=dir_name, prefix="test_get_size", suffix=".test") as f,
        ):
            # Write random bytes with specified size
            f.write(os.urandom(size))

            # Flush from buffer
            f.flush()
            # Move pointer to start of file
            f.seek(0)

            assert (
                size
                # Check on a file
                == base_collector._get_size(Pathlib(f.name))
                # Check on dir
                == base_collector._get_size(Pathlib(dir_name))
                # Check in glob with star
                # == base_collector._get_size(Pathlib(dir_name + "/*"))
                # Check in glob with brackets
                # == base_collector._get_size(Pathlib(dir_name + "/[!mac]*"))
            )

            assert (
                0
                # Check in glob with star
                == base_collector._get_size(Pathlib(f.name + "/*"))
                # Negative check in glob with brackets
                == base_collector._get_size(Pathlib(dir_name + "/[!test]*"))
            )

    @pytest.mark.parametrize("is_file", [True, False])
    def test_get_size_errors(self, is_file: bool, base_collector: _Collector, monkeypatch: MonkeyPatch):
        """Test errors in :meth:`mac_cleanup.core._Collector._get_size`"""

        # Check path doesn't exist in glob
        assert base_collector._get_size(Pathlib("~/Documents")) == 0

        error = PermissionError

        # Dummy path raising error
        def dummy_path_stat(console_self: Pathlib, follow_symlinks: bool) -> None:  # noqa  # noqa  # noqa
            raise error

        # Dummy Pathlib.is_file
        dummy_is_file: Callable[[Pathlib], bool] = lambda path_self: is_file

        # Dummy Pathlib.exists (always True)
        dummy_exists: Callable[[Pathlib], bool] = lambda path_self: True

        # Dummy Pathlib.glob (always one empty path)
        dummy_glob: Callable[[Pathlib, str], list[Pathlib]] = lambda path_self, pattern: [Pathlib()]

        # Simulate path is file and exist
        monkeypatch.setattr("mac_cleanup.core.Path_.is_file", dummy_is_file)
        monkeypatch.setattr("mac_cleanup.core.Path_.exists", dummy_exists)

        # Simulate glob being opened
        monkeypatch.setattr("mac_cleanup.core.Path_.glob", dummy_glob)

        # Simulate error being raised
        monkeypatch.setattr("mac_cleanup.core.Path_.stat", dummy_path_stat)

        # Check PermissionError
        base_collector._get_size(Pathlib("/"))

        # Check FileNotFoundError
        error = FileNotFoundError
        base_collector._get_size(Pathlib("/"))

    @pytest.mark.parametrize("size_multiplier", [0, 1, 1024])
    def test_extract_paths(self, size_multiplier: int, base_collector: _Collector, monkeypatch: MonkeyPatch):
        """Test :meth:`mac_cleanup.core._Collector._extract_paths`"""

        # Get size in bytes
        size = 1024 * size_multiplier

        # Dummy get_size
        dummy_get_size: Callable[[_Collector, Pathlib], float] = lambda clc_self, path: size

        # Simulate get_size with specified size
        monkeypatch.setattr("mac_cleanup.core._Collector._get_size", dummy_get_size)

        # Simulate stuff in execute_list
        monkeypatch.setattr(base_collector, "_execute_list", [Unit(message="test", modules=[Path("~/test")])])

        # Call _extract_paths
        paths = list(base_collector._extract_paths())

        # Check results
        assert len(paths) == 1
        assert paths[0][0] == Path("~/test").get_path
        assert paths[0][1] == size

    def test_extract_paths_error(self, base_collector: _Collector, monkeypatch: MonkeyPatch):
        """Test errors in :meth:`mac_cleanup.core._Collector._extract_paths`"""

        # Dummy get size raising KeyboardInterrupt
        def dummy_get_size(clc_self: _Collector, path: Pathlib) -> float:  # noqa  # noqa
            raise KeyboardInterrupt

        # Simulate get_size with error
        monkeypatch.setattr("mac_cleanup.core._Collector._get_size", dummy_get_size)

        # Simulate stuff in execute_list
        monkeypatch.setattr(base_collector, "_execute_list", [Unit(message="test", modules=[Path("~/test")])])

        # Check prematurely exit return 0
        # Call _extract_paths
        paths = list(base_collector._extract_paths())

        # Check results
        assert len(paths) == 0
