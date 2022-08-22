from . import *
from .utils import cmd, bytes_to_human, catch_exception
from .console import console, print_panel
from .config import load_config

t = Collector()


@catch_exception
def main() -> None:
    # Clear console at the start
    console.clear()

    # Sets custom modules' path if user prompted to and exits
    if args.modules:
        from .config import set_custom_path

        set_custom_path()
        raise KeyboardInterrupt

    # Loads all modules
    load_config(configuration_needed=args.configure)

    # Exits if configuration was requested
    if args.configure:
        raise KeyboardInterrupt

    def count_free_space(
    ) -> int:
        return int(cmd("df / | tail -1 | awk '{print $4}'"))

    def cleanup(
    ) -> None:
        from rich.progress import track

        # Free space before the run
        oldAvailable = count_free_space()

        # Ask for password input in terminal (sudo -E)
        # Raises AssertionError if prompt fails
        assert cmd("sudo -E whoami") == "root"

        for module in t.execute_list:
            if not module.msg or not module.unit_list:
                continue

            for unit in track(
                    module.unit_list,
                    description=module.msg,
                    transient=True,
                    total=len(module.unit_list)
            ):
                # Doesn't execute dry run query
                if unit.dry:
                    continue

                # If not cmd then add "sudo rm -rf"
                if not unit.cmd:
                    unit.command = "sudo rm -rf {0}".format(unit.command.replace(" ", "\ "))  # type: ignore # noqa ignore W605

                # There are no tasks w/o command
                cmd(unit.command)

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

        freed_space = bytes_to_human(t.count_dry())

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
        # At least Cyrillic symbols will crash rich.Confirm
        except UnicodeDecodeError:
            console.clear()
            console.print(
                "Do not enter symbols that can't be decoded to utf8",
                style="danger",
            )
            console.print("Exiting...")


if __name__ == "__main__":
    main()
