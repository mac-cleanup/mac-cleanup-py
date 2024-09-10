"""Wrapper for handling all errors in entry point."""

from functools import wraps
from typing import Any, Callable, Iterable, Optional, Type, TypeVar, overload

T = TypeVar("T", bound=Callable[..., Any])

_iterable_exception = tuple[Type[BaseException]] | list[Type[BaseException]]
_exception = Type[BaseException] | _iterable_exception


class ErrorHandler:
    """Decorator for catching exceptions and printing logs."""

    def __init__(self, exception: Optional[_exception] = None, exit_on_exception: bool = False):
        # Sets default exception (empty tuple) if none was provided
        if exception is None:
            self.exception: _iterable_exception = tuple[Type[BaseException]]()
        # Changes exception class to tuple if it's class
        elif not isinstance(exception, Iterable):
            self.exception = (exception,)
        else:
            self.exception = exception

        # Sets exit_on_exception
        self.exit_on_exception = exit_on_exception

    def __call__(self, func: T) -> Callable[..., Optional[T]]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Optional[T]:
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                from mac_cleanup.console import console

                # Print exit message
                console.print("\n[warning]Exiting...")

                # Exit if prompted
                if self.exit_on_exception:
                    exit(0)
            # Exclude SystemExit from BaseException clause
            except SystemExit as err:
                raise err
            # Catch all other errors
            except BaseException as err:
                # Clause for not expected error
                if type(err) not in self.exception:
                    from logging import basicConfig, getLogger

                    from rich.logging import RichHandler

                    from mac_cleanup.console import console

                    # Set logger config
                    basicConfig(
                        level="ERROR",
                        format="%(message)s",
                        datefmt="[%X]",
                        handlers=[RichHandler(rich_tracebacks=True)],
                    )

                    # Get logger
                    log = getLogger("EntryPoint")

                    # Log error
                    log.exception("Unexpected error occurred")

                    # Print exit message
                    console.print("\n[danger]Exiting...")

                    # Exit if prompted
                    if self.exit_on_exception:
                        exit(1)

        return wrapper


@overload
def catch_exception(
    func: T, exception: Optional[_exception] = ..., exit_on_exception: bool = ...
) -> T: ...  # pragma: no cover (coverage marks line as untested)


@overload
def catch_exception(
    func: None = ..., exception: Optional[_exception] = ..., exit_on_exception: bool = ...
) -> ErrorHandler: ...  # pragma: no cover (coverage marks line as untested)


def catch_exception(
    func: Optional[T] = None, exception: Optional[_exception] = None, exit_on_exception: bool = True
) -> ErrorHandler | Callable[..., Optional[T]]:
    """
    Decorator for catching exceptions and printing logs.

    :param func: Function to be decorated
    :param exception: Expected exception(s)
    :param exit_on_exception: If True, exit after unexpected exception was handled
    :return: Decorated function
    """

    err_handler_instance: ErrorHandler = ErrorHandler(exception=exception, exit_on_exception=exit_on_exception)

    if func:
        err_handler_call: Callable[..., Optional[T]] = err_handler_instance(func)
        return err_handler_call

    return err_handler_instance
