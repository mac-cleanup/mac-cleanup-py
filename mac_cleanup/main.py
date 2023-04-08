from pathlib import Path

from mac_cleanup.core import _Collector
from mac_cleanup.core_modules import BaseModule
from mac_cleanup.parser import args
from mac_cleanup.console import console, print_panel
from mac_cleanup.config import Config
from mac_cleanup.utils import cmd, bytes_to_human
from mac_cleanup.error_handling import catch_exception


config_path = Path.home().joinpath(".mac_cleanup_py")
base_collector = _Collector()


@catch_exception
def main() -> None:
    # Clear console at the start
    console.clear()

    # Get config
    config = Config(config_path_=config_path)

    # Sets custom modules' path if user prompted to and exits
    if args.custom_path:
        # Set custom path and exit
        config.set_custom_path()

    # Check config
    config(configuration_prompted=args.configure)

    def count_free_space(
    ) -> float:
        return float(cmd("df / | tail -1 | awk '{print $4}'"))

    def cleanup() -> None:
        from mac_cleanup.progress import ProgressBar

        # Free space before the run
        free_space_before = count_free_space()

        for unit in base_collector._execute_list:  # noqa
            for module in ProgressBar.wrap_iter(
                    unit.modules,
                    description=unit.message,
                    total=len(unit.modules)
            ):
                # Fix type hinting
                module: BaseModule

                # Call for module execution
                module._execute()  # noqa

        # Free space after the run
        free_space_after = count_free_space()

        # Print results
        print_panel(
            text=f"Removed - [success]{bytes_to_human((free_space_after - free_space_before) * 1024)}",
            title="[info]Success",
        )

    # Handle dry runs
    if args.dry_run:
        from rich.prompt import Confirm

        freed_space = bytes_to_human(
            base_collector._count_dry()  # noqa
        )

        print_panel(
            text=f"Approx [success]{freed_space}[/success] will be cleaned",
            title="[info]Dry run results",
        )

        try:
            continue_cleanup = Confirm.ask("Continue?", show_default=False, default="y")
        # Cyrillic symbols may crash rich.Confirm
        except UnicodeDecodeError:
            console.clear()
            console.print(
                "Do not enter symbols that can't be decoded to UTF-8",
                style="danger",
            )
            console.print("Exiting...")
            return

        console.clear()

        # Exit if user doesn't want to continue
        if not continue_cleanup:
            console.print("Exiting...")
            return

    # Clean stuff up
    cleanup()


if __name__ == "__main__":
    main()
