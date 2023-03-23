"""Console argument parser configuration"""
from typing import final

from argparse import ArgumentParser, RawTextHelpFormatter

import attr

from mac_cleanup.__version__ import __version__


@final
@attr.s(slots=True)
class Args:
    dry_run: bool = attr.ib(default=False)
    update: bool = attr.ib(default=False)
    configure: bool = attr.ib(default=False)
    custom_path: bool = attr.ib(default=False)


parser = ArgumentParser(
    description=f"""\
    A Mac Cleanup Utility in Python
    {__version__}
    https://github.com/mac-cleanup/mac-cleanup-py\
    """,
    formatter_class=RawTextHelpFormatter,
)

parser.add_argument(
    "-n", "--dry-run",
    help="Dry run without deleting stuff",
    action="store_true"
)

parser.add_argument(
    "-u", "--update",
    help="Update HomeBrew on cleanup",
    action="store_true"
)

parser.add_argument(
    "-c", "--configure",
    help="Configure default and custom modules",
    action="store_true"
)

parser.add_argument(
    "-p", "--custom",
    help="Specify path for custom modules",
    action="store_true"
)

args = Args()
parser.parse_args(namespace=args)

# args.dry_run = True  # debug
# args.configure = True  # debug
# args.modules = True  # debug
