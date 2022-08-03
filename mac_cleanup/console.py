from argparse import ArgumentParser, RawTextHelpFormatter
from rich.console import Console

parser = ArgumentParser(
    description=
    """\
    A Mac Cleanup Utility in Python
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

args = parser.parse_args()
# args.dry_run = True

console = Console()
