"""All core modules."""
from abc import ABC, abstractmethod
from pathlib import Path as Path_
from typing import Final, Optional, TypeVar, final

from beartype import beartype  # pyright: ignore [reportUnknownVariableType]

from mac_cleanup.progress import ProgressBar
from mac_cleanup.utils import check_deletable, check_exists, cmd

T = TypeVar("T")


class BaseModule(ABC):
    """Base abstract module."""

    __prompt: bool = False
    __prompt_message: str = "Do you want to proceed?"

    @beartype
    def with_prompt(self: T, message_: Optional[str] = None) -> T:
        """
        Execute command with user prompt.

        :param message_: Message to be shown on prompt
        :return: Instance of self from
        :class: `BaseModule`
        """

        # Can't be solved without typing.Self
        self.__prompt = True  # pyright: ignore [reportGeneralTypeIssues]

        if message_:
            # Can't be solved without typing.Self
            self.__prompt_message = message_  # pyright: ignore [reportGeneralTypeIssues]

        return self

    @abstractmethod
    def _execute(self) -> bool:
        """Base exec with check for prompt :return: True on successful prompt."""

        # Call prompt if needed
        if self.__prompt:
            # Skip on negative prompt
            return ProgressBar.prompt(prompt_text=self.__prompt_message, prompt_title="Module requires attention")

        return True


class _BaseCommand(BaseModule):
    """Base Command with basic command methods."""

    __has_root: bool = False

    @beartype
    def __init__(self, command_: Optional[str]):
        # Ask for password input in terminal (sudo -E)
        # Raises AssertionError if prompt fails
        if not self.__has_root:
            # Get root
            assert cmd("sudo -E whoami") == "root"

            # Set global root attr
            _BaseCommand.__has_root = True

        self.__command: Final[Optional[str]] = command_

    @property
    def get_command(self) -> Optional[str]:
        """Get command specified to the module."""

        return self.__command

    @abstractmethod
    def _execute(self, **kwargs: bool) -> Optional[str]:
        """
        Execute the command specified.

        :param ignore_errors_: Ignore errors during execution
        :return: Command execution results based on specified parameters
        """

        # Skip if there is no command
        if not self.__command:
            return

        # Skip on negative prompt
        if not super()._execute():
            return

        # Execute command
        return cmd(command=self.__command, ignore_errors=kwargs.get("ignore_errors", True))


@final
class Command(_BaseCommand):
    """Collector list unit for command execution."""

    __ignore_errors: bool = True

    def with_errors(self) -> "Command":
        """Return errors in exec output :return: :class:`Command`"""

        self.__ignore_errors = False

        return self

    def _execute(self) -> Optional[str]:
        return super()._execute(ignore_errors=self.__ignore_errors)


@final
class Path(_BaseCommand):
    """Collector list unit for cleaning paths."""

    __dry_run_only: bool = False

    @beartype
    def __init__(self, path: str):
        self.__path: Final[Path_] = Path_(path).expanduser()

        tmp_command = "rm -rf '{path}'".format(path=self.__path.as_posix())

        super().__init__(command_=tmp_command)

    @property
    def get_path(self) -> Path_:
        """Get path specified to the module."""

        return self.__path

    def dry_run_only(self) -> "Path":
        """Set module to only count size in dry runs :return: :class:`Path`"""

        self.__dry_run_only = True

        return self

    def _execute(self) -> Optional[str]:
        """Delete specified path :return: Command execution results based on specified
        parameters.
        """

        if self.__dry_run_only:
            return

        # Skip if path is not deletable or undefined
        if not all([check_deletable(path=self.__path), check_exists(path=self.__path, expand_user=False)]):
            return

        return super()._execute()  # Always ignore errors
