from mac_cleanup import __version__
from argparse import ArgumentParser, RawTextHelpFormatter
from rich.console import Console
from rich.theme import Theme


parser = ArgumentParser(
    description=
    f"""\
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
    help="Launch modules configuration",
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

custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
})  # WIP
console = Console(theme=custom_theme)
