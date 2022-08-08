from rich.progress import track
from rich.prompt import Confirm
from rich.panel import Panel
from mac_cleanup.utils import CleanUp, cmd, bytes_to_human, catch_exception
from mac_cleanup.console import console, args
from mac_cleanup.config import load_config


t = CleanUp()


@catch_exception
def main() -> None:
    # Loads all modules
    load_config(configuration_needed=args.configure)

    # Exits if configuration was requested
    if args.configure:
        raise KeyboardInterrupt

    def count_free_space():
        return int(cmd("df / | tail -1 | awk '{print $4}'"))

    def cleanup():
        # Free space before the run
        oldAvailable = count_free_space()

        # Ask for password input in terminal
        cmd("sudo -E echo")

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

        # Launch brew additional cleanup & repair
        for brew_task in track(
                ["brew cleanup -s", "brew tap --repair"],
                description="Cleaning Brew",
                transient=True,
                total=2,
        ):
            cmd(brew_task)

        # Free space after the run
        newAvailable = count_free_space()

        # Print results
        console.print(
            Panel(
                f"Removed - [info]{bytes_to_human((newAvailable - oldAvailable) * 1024)}",
                title="Success",
                title_align="center",
            )
        )
    # Straight to clean up if not dry run
    if not args.dry_run:
        cleanup()
    else:
        freed_space = bytes_to_human(t.count_dry())

        console.print(f"Approx {freed_space} will be cleaned")
        if Confirm.ask("Continue?"):
            console.clear()
            cleanup()
        else:
            console.clear()
            console.print("Exiting...")


if __name__ == "__main__":
    main()
