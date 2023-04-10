"""Test global error handler"""
from typing import Iterable, Type

import pytest
from _pytest.capture import CaptureFixture
from _pytest.logging import LogCaptureFixture

from mac_cleanup.error_handling import _exception  # noqa
from mac_cleanup.error_handling import catch_exception


class TestErrorHandler:
    @pytest.mark.parametrize("raised_exception", [KeyboardInterrupt, BaseException])
    def test_with_func(
        self, raised_exception: Type[BaseException], capsys: CaptureFixture[str], caplog: LogCaptureFixture
    ):
        """Test wrapping functions without calling wrapper"""

        # Dummy callable wrapped in handler raised exception
        @catch_exception
        def dummy_callable() -> None:
            raise raised_exception

        # Call dummy callable and expect exit
        with pytest.raises(SystemExit):
            dummy_callable()

        # Get stdout
        captured_stdout = capsys.readouterr().out

        # Check correct stdout
        assert "\nExiting...\n" in captured_stdout

        # Get logger output
        captured_log = caplog.text

        # No logger output on KeyboardInterrupt
        expected_log = "Unexpected error occurred" if raised_exception is BaseException else ""

        # Check correct logger output
        assert expected_log in captured_log

    @pytest.mark.parametrize("raised_exception", [KeyboardInterrupt, BaseException])
    def test_no_func(
        self, raised_exception: Type[BaseException], capsys: CaptureFixture[str], caplog: LogCaptureFixture
    ):
        """Test wrapping functions with calling wrapper"""

        # Dummy callable wrapped in handler raised exception
        @catch_exception()
        def dummy_callable() -> None:
            raise raised_exception

        # Call dummy callable and expect exit
        with pytest.raises(SystemExit):
            dummy_callable()

        # Get stdout
        captured_stdout = capsys.readouterr().out

        # Check correct stdout
        assert "\nExiting...\n" in captured_stdout

        # Get logger output
        captured_log = caplog.text

        # No logger output on KeyboardInterrupt
        expected_log = "Unexpected error occurred" if raised_exception is BaseException else ""

        # Check correct logger output
        assert expected_log in captured_log

    @pytest.mark.parametrize("raised_exception", [KeyboardInterrupt, BaseException])
    def test_no_exit_on_exception(
        self, raised_exception: Type[BaseException], capsys: CaptureFixture[str], caplog: LogCaptureFixture
    ):
        """Test wrapping functions without exiting on caught stuff"""

        # Dummy callable wrapped in handler raised exception
        @catch_exception(exit_on_exception=False)
        def dummy_callable() -> None:
            raise raised_exception

        # Call dummy callable and expect no errors
        dummy_callable()

        # Get stdout
        captured_stdout = capsys.readouterr().out

        # Check correct stdout
        assert "\nExiting...\n" in captured_stdout

        # Get logger output
        captured_log = caplog.text

        # No logger output on KeyboardInterrupt
        expected_log = "Unexpected error occurred" if raised_exception is BaseException else ""

        # Check correct logger output
        assert expected_log in captured_log

    @pytest.mark.parametrize("custom_exception", [(ValueError, KeyError), [ValueError, KeyError], BaseException])
    def test_custom_exceptions(
        self, custom_exception: _exception, capsys: CaptureFixture[str], caplog: LogCaptureFixture
    ):
        """Test wrapping functions with providing expected exceptions"""

        # Dummy callable wrapped in handler raised exception
        @catch_exception(exception=custom_exception)
        def dummy_callable() -> None:
            raise (custom_exception if not isinstance(custom_exception, Iterable) else custom_exception[0])

        # Call dummy callable and expect no errors
        dummy_callable()

        # Get stdout
        captured_stdout = capsys.readouterr().out

        # Check correct stdout
        assert captured_stdout == ""

        # Get logger output
        captured_log = caplog.text

        # Check correct logger output
        assert captured_log == ""

    @pytest.mark.parametrize("exit_code", [0, 1])
    def test_exit_raised(self, exit_code: int, capsys: CaptureFixture[str], caplog: LogCaptureFixture):
        """Test wrapping functions raising SystemExit"""

        # Dummy callable wrapped in handler raised SystemExit
        @catch_exception
        def dummy_callable() -> None:
            exit(exit_code)

        # Call dummy callable and expect exit
        with pytest.raises(SystemExit):
            dummy_callable()

        # Get stdout
        captured_stdout = capsys.readouterr().out

        # Check correct stdout
        assert captured_stdout == ""

        # Get logger output
        captured_log = caplog.text

        # Check correct logger output
        assert captured_log == ""
