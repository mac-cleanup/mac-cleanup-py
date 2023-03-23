"""All core modules"""
from typing import final, Final, Optional

from beartype import beartype

from abc import ABC, abstractmethod

from pathlib import Path as Path_

from mac_cleanup.progress import ProgressBar
from mac_cleanup.utils import cmd, check_deletable, check_exists


@beartype
class BaseModule(ABC):
    """Base abstract module"""

    __prompt: bool = False
    __prompt_message: str = "Do you want to proceed?"

    def with_prompt(
            self,
            message_: Optional[str] = None,
            /
    ) -> 'BaseModule':
        """
        Execute command with user prompt
            :param message_: Message to be shown on prompt
            :return: :class:`BaseModule`
        """

        self.__prompt = True

        if message_:
            self.__prompt_message = message_

        return self

    @abstractmethod
    def _execute(self) -> bool:
        """
        Base exec with check for prompt
            :return: True on successful prompt
        """

        # Call prompt if needed
        if self.__prompt:
            # Skip on negative prompt
            return ProgressBar.prompt(
                    prompt_=self.__prompt_message
            )

        return True


@beartype
class _BaseCommand(BaseModule):
    """Base Command with basic command methods"""

    __has_root: bool = False

    def __init__(
            self,
            command_: Optional[str]
    ):
        # Ask for password input in terminal (sudo -E)
        # Raises AssertionError if prompt fails
        if not self.__has_root:
            # Get root
            assert cmd("sudo -E whoami") == "root"

            # Set global root attr
            _BaseCommand.__has_root = True

        self.__command: Final[Optional[str]] = command_

    @abstractmethod
    def _execute(
            self,
            **kwargs,
    ) -> Optional[str]:
        """
        Execute the command specified
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
        return cmd(
            command=self.__command,
            ignore_errors=kwargs.get("ignore_errors", True)
        )


@beartype
@final
class Command(_BaseCommand):
    """Collector list unit for command execution"""

    __ignore_errors: bool = True

    def with_errors(self) -> 'Command':
        """
        Return errors in exec output
            :return: :class:`Command`
        """

        self.__ignore_errors = False

        return self

    def _execute(
            self,
            *,
            ignore_errors_: bool = True
    ) -> Optional[str]:
        return super()._execute(ignore_errors=self.__ignore_errors)


@beartype
@final
class Path(_BaseCommand):
    """Collector list unit for cleaning paths"""

    __dry_run_only: bool = False

    def __init__(
            self,
            path_: str
    ):
        self.__path: Final[Path_] = Path_(path_.replace(" ", "\\ ")).expanduser()

        tmp_command: Optional[str] = None

        if self.__path.as_posix():
            tmp_command = "rm -rf {path}".format(path=self.__path.as_posix())

        super().__init__(command_=tmp_command)

    def dry_run_only(self) -> 'Path':
        """
        Set module to only count size in dry runs
            :return: :class:`Path`
        """

        self.__dry_run_only = True

        return self

    def _execute(self) -> None:
        """
        Delete specified path
            :return: Command execution results based on specified parameters
        """

        if self.__dry_run_only:
            return

        # Skip if path is not deletable or undefined
        if (
                check_deletable(path=self.__path)
                and not check_exists(path=self.__path)
        ):
            return

        super()._execute()
