"""Modified rich progress bar"""
from typing import Union, Iterable, Sequence, Optional

from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn, ProgressType
from rich.prompt import Confirm

from mac_cleanup.console import console


class __ProgressBar(Progress):
    def __init__(self):
        # Call parent init w/ default stuff
        super().__init__(
            SpinnerColumn(),
            *Progress.get_default_columns(),
            TimeElapsedColumn(),
            console=console,
            transient=True,
        )

    def prompt(
            self,
            prompt_: str,
            password: bool = False,
            choices: Optional[list[str]] = None,
            show_default: bool = True,
            show_choices: bool = True,
    ) -> bool:
        """
        Stops progress bar to show prompt to user
            :param prompt_: Prompt text
            :param password: Enable password input. Defaults to False.
            :param choices: A list of valid choices. Defaults to None.
            :param show_default: Show default in prompt. Defaults to True.
            :param show_choices: Show choices in prompt. Defaults to True.
            :return: True on successful prompt
        """

        # Stop refreshing progress bar
        self.stop()

        # Ask question
        answer = Confirm.ask(
            prompt=prompt_,
            console=self.console,
            password=password,
            choices=choices,
            show_default=show_default,
            show_choices=show_choices,
        )

        self.console.clear()
        self.console.clear_live()  # TODO: check if needed

        # Resume refreshing progress bar
        self.start()

        return answer

    def wrap_iter(
            self,
            sequence: Union[Iterable[ProgressType], Sequence[ProgressType]],
            total: Optional[float] = None,
            description: str = "Working..."
    ) -> Iterable[ProgressType]:
        """
        Wrapper other :func:`rich.progress.track`
            :param sequence: Sequence (must support "len") you wish to iterate over.
            :param total: Total number of steps. Default is len(sequence).
            :param description: Description of task show next to progress bar. Defaults to "Working".
            :return: An iterable of the values in the sequence
        """

        with self:
            yield from self.track(
                sequence,
                total=total,
                description=description
            )


# ProgressBar instance for all project
ProgressBar = __ProgressBar()
