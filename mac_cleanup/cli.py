from rich.progress import track
from mac_cleanup.utils import CleanUp, cmd, bytes_to_human, catch_exception
from mac_cleanup.console import console, args
from mac_cleanup.modules import load_default

t = CleanUp()
load_default()


@catch_exception
def main() -> None:
    def count_free_space():
        return int(cmd("df / | tail -1 | awk '{print $4}'"))

    def cleanup():
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
                if task["type"] == "dry":
                    continue
                if task["type"] == "path":
                    task["main"] = f"sudo rm -rf {task['main']}"
                cmd(task["main"])

        for brew_task in track(
                ["brew cleanup -s", "brew tap --repair"],
                description="Cleaning Brew",
                transient=True,
                total=2,
        ):
            cmd(brew_task)
        console.print("Success")
        newAvailable = count_free_space()
        console.print("Removed -", bytes_to_human((newAvailable - oldAvailable) * 1024))

    if not args.dry_run:
        cleanup()
    else:
        freed_space = bytes_to_human(t.count_dry())

        while True:
            console.print(f"Approx {freed_space} will be cleaned")
            if console.input("Continue? [enter]").strip() == "":
                console.clear()
                cleanup()
                return
            else:
                console.clear()
                console.print("Don't recognize the input, try again...")


if __name__ == "__main__":
    main()
