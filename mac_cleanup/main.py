from mac_cleanup.collector import _BaseCollector
from mac_cleanup.core import BaseModule
from mac_cleanup.utils import cmd, bytes_to_human
# from mac_cleanup.utils import catch_exception
from mac_cleanup.console import args, console, print_panel
from mac_cleanup.config import load_config

t = _BaseCollector()


# @catch_exception
def main() -> None:  # TODO: rewrite
    # Clear console at the start
    console.clear()

    # Sets custom modules' path if user prompted to and exits
    if args.modules:
        from mac_cleanup.config import set_custom_path

        # Set custom path
        set_custom_path()

        # Exit
        raise KeyboardInterrupt

    # Load modules
    load_config(configuration_needed=args.configure)

    # Exits if configuration was requested
    if args.configure:  # TODO: move logic here
        raise KeyboardInterrupt

    def count_free_space(
    ) -> int:
        return int(cmd("df / | tail -1 | awk '{print $4}'"))

    def cleanup(
    ) -> None:
        from mac_cleanup.progress import ProgressBar

        # Free space before the run
        oldAvailable = count_free_space()

        # Ask for password input in terminal (sudo -E)
        # Raises AssertionError if prompt fails
        assert cmd("sudo -E whoami") == "root"

        for unit in t._execute_list:
            for module in ProgressBar.wrap_iter(
                    unit.modules,
                    description=unit.message,
                    transient=True,
                    total=len(unit.modules)
            ):
                # Fix type hinting
                module: BaseModule

                # Call for module execution
                module._execute()

        # Free space after the run
        newAvailable = count_free_space()

        # Print results
        print_panel(
            text=f"Removed - [success]{bytes_to_human((newAvailable - oldAvailable) * 1024)}",
            title="[info]Success",
        )

    # Straight to clean up if not dry run
    if not args.dry_run:
        cleanup()
    else:
        from rich.prompt import Confirm

        freed_space = bytes_to_human(t._count_dry())

        print_panel(
            text=f"Approx [success]{freed_space}[/success] will be cleaned",
            title="[info]Dry run results",
        )

        try:
            if Confirm.ask("Continue?", show_default=False, default="y"):
                console.clear()
                cleanup()
            else:
                console.clear()
                console.print("Exiting...")

        # Cyrillic symbols may crash rich.Confirm
        except UnicodeDecodeError:
            console.clear()
            console.print(
                "Do not enter symbols that can't be decoded to utf-8",
                style="danger",
            )
            console.print("Exiting...")


if __name__ == "__main__":
    main()
