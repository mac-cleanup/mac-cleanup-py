from mac_cleanup.utils import CleanUp, cmd, bytes_to_human, catch_exception
from mac_cleanup.console import console, args, print_panel
from mac_cleanup.config import load_config

t = CleanUp()


@catch_exception
def main() -> None:
    # Clear console at the start
    console.clear()

    # Sets custom modules' path if user prompted to and exits
    if args.modules:
        from mac_cleanup.config import set_custom_path

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

        # Ask for password input in terminal
        # Raises AssertionError if prompt fails
        assert cmd("sudo -E whoami") == "root"

        for item in t.execute_list:
            if not item.get("msg") or not item.get("exec_list"):
                continue

            for task in track(
                    item["exec_list"],
                    description=item["msg"],
                    transient=True,
                    total=len(item["exec_list"])
            ):
                # Doesn't execute dry run query
                if task["type"] == "dry":
                    continue
                # If type == "path" add rm -rf
                if task["type"] == "path":
                    task["main"] = "sudo rm -rf {0}".format(task["main"].replace(" ", "\ "))
                # There are no tasks w/o main
                cmd(task["main"])

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
        if Confirm.ask("Continue?", show_default=False, default="y"):
            console.clear()
            cleanup()
        else:
            console.clear()
            console.print("Exiting...")


if __name__ == "__main__":
    main()
