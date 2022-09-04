from .__version__ import __version__
from argparse import ArgumentParser, RawTextHelpFormatter
from rich.console import Console
from rich.theme import Theme

parser = ArgumentParser(
    description=f"""\
    A Mac Cleanup Utility in Python
    {__version__}
    https://github.com/mac-cleanup/mac-cleanup-py\
    """,
    formatter_class=RawTextHelpFormatter,
)

parser.add_argument(
    "-d", "--dry-run",
    help="Shows approx space to be cleaned",
    action="store_true"
)

parser.add_argument(
    "-u", "--update",
    help="Script will update brew while cleaning",
    action="store_true"
)

parser.add_argument(
    "-c", "--configure",
    help="Opens modules' configuration screen",
    action="store_true"
)

parser.add_argument(
    "-m", "--modules",
    help="Specify custom modules' path",
    action="store_true"
)

args = parser.parse_args()
# args.dry_run = True  # debug
# args.configure = True  # debug
# args.modules = True  # debug

custom_theme = Theme({
    "info": "cyan",
    "warning": "magenta",
    "danger": "bold red",
    "success": "bold green",
})

console = Console(theme=custom_theme)


def print_panel(
        text: str,
        title: str = "",
) -> None:  # pragma: no cover
    """
    Prints a rich panel with the given text

    Args:
        text: Text to print in the panel
        title: Title of the panel
    """
    from rich.panel import Panel
    from rich.text import Text

    console.print(
        Panel(
            Text.from_markup(
                text,
                justify="center"
            ),
            subtitle=title,
            subtitle_align="right",
        )
    )
