from os import getenv
from rich.progress import track

from mac_cleanup.utils import CleanUp, cmd, bytes_to_human, check_exists, catch_exception
from mac_cleanup.console import console, args

t = CleanUp()


t.msg("Emptying the Trash 🗑 on all mounted volumes and the main HDD...")
t.collect("/Volumes/*/.Trashes/*")
t.collect("~/.Trash/*")

t.msg("Clearing System Cache Files...")
t.collect("/Library/Caches/*")
t.collect("/System/Library/Caches/*")
t.collect("~/Library/Caches/*")
t.collect("/private/var/folders/bh/*/*/*/*")

t.msg("Clearing System Log Files...")
t.collect("/private/var/log/asl/*.asl")
t.collect("/Library/Logs/DiagnosticReports/*")
t.collect("/Library/Logs/CreativeCloud/*")
t.collect("/Library/Logs/Adobe/*")
t.collect("/Library/Logs/adobegc.log")
t.collect("~/Library/Containers/com.apple.mail/Data/Library/Logs/Mail/*")
t.collect("~/Library/Logs/CoreSimulator/*")

if check_exists("~/Library/Logs/JetBrains/"):
    t.msg("Clearing all application log files from JetBrains...")
    t.collect("~/Library/Logs/JetBrains/*/")

if check_exists("~/Library/Application Support/Adobe/"):
    t.msg("Clearing Adobe Cache Files...")
    t.collect("~/Library/Application Support/Adobe/Common/Media Cache Files/*")

if check_exists("~/Library/Application Support/Google/Chrome/"):
    t.msg("Clearing Google Chrome Cache Files...")
    t.collect("~/Library/Application Support/Google/Chrome/Default/Application Cache/*")

t.msg("Cleaning up iOS Applications...")
t.collect("~/Music/iTunes/iTunes Media/Mobile Applications/*")

t.msg("Removing iOS Device Backups...")
t.collect("~/Library/Application Support/MobileSync/Backup/*")

t.msg("Cleaning up XCode Derived Data and Archives...")
t.collect("~/Library/Developer/Xcode/DerivedData/*")
t.collect("~/Library/Developer/Xcode/Archives/*")
t.collect("~/Library/Developer/Xcode/iOS Device Logs/*")

if cmd("type 'xcrun'"):
    t.msg("Cleaning up iOS Simulators...")
    t.collect("osascript -e 'tell application 'com.apple.CoreSimulator.CoreSimulatorService' to quit'", command=True)
    t.collect("osascript -e 'tell application 'iOS Simulator' to quit'", command=True)
    t.collect("osascript -e 'tell application 'Simulator' to quit'", command=True)
    t.collect("xcrun simctl shutdown all", command=True)
    t.collect("xcrun simctl erase all", command=True)
    # For dry_run
    t.collect("~/Library/Developer/CoreSimulator/Devices/*/data/[!Library|var|tmp|Media]*", dry=True)
    t.collect(
        "/Users/wah/Library/Developer/CoreSimulator/Devices/*/data/Library/"
        "[!PreferencesCaches|Caches|AddressBook|Trial]*",
        dry=True
    )
    t.collect("~/Library/Developer/CoreSimulator/Devices/*/data/Library/Caches/*", dry=True)
    t.collect("~/Library/Developer/CoreSimulator/Devices/*/data/Library/AddressBook/AddressBook*", dry=True)

# Support deleting Dropbox Cache if they exist
if check_exists("~/Dropbox"):
    t.msg("Clearing Dropbox 📦 Cache Files...")
    t.collect("~/Dropbox/.dropbox.cache/*")

if check_exists("~/Library/Application Support/Google/DriveFS/"):
    t.msg("Clearing Google Drive File Stream Cache Files...")
    t.collect("killall 'Google Drive File Stream'", command=True)
    t.collect("~/Library/Application Support/Google/DriveFS/[0-9a-zA-Z]*/content_cache")

if cmd("type 'composer'"):
    t.msg("Cleaning up composer...")
    t.collect("composer clearcache --no-interaction", command=True)
    # For dry_run
    t.collect("~/Library/Caches/composer", dry=True)

# Deletes Steam caches, logs, and temp files
if check_exists("~/Library/Application Support/Steam/"):
    t.msg("Clearing Steam Cache, Log, and Temp Files...")
    t.collect("~/Library/Application Support/Steam/appcache")
    t.collect("~/Library/Application Support/Steam/depotcache")
    t.collect("~/Library/Application Support/Steam/logs")
    t.collect("~/Library/Application Support/Steam/steamapps/shadercache")
    t.collect("~/Library/Application Support/Steam/steamapps/temp")
    t.collect("~/Library/Application Support/Steam/steamapps/download")

# Deletes Minecraft logs
if check_exists("~/Library/Application Support/minecraft"):
    t.msg("Clearing Minecraft Cache and Log Files...")
    t.collect("~/Library/Application Support/minecraft/logs")
    t.collect("~/Library/Application Support/minecraft/crash-reports")
    t.collect("~/Library/Application Support/minecraft/webcache")
    t.collect("~/Library/Application Support/minecraft/webcache2")
    t.collect("~/Library/Application Support/minecraft/crash-reports")
    t.collect("~/Library/Application Support/minecraft/*.log")
    t.collect("~/Library/Application Support/minecraft/launcher_cef_log.txt")
    if check_exists("~/Library/Application Support/minecraft/.mixin.out"):
        t.collect("~/Library/Application Support/minecraft/.mixin.out")

# Deletes Lunar Client logs (Minecraft alternate client)
if check_exists("~/.lunarclient"):
    t.msg("Deleting Lunar Client logs and caches...")
    t.collect("~/.lunarclient/game-cache")
    t.collect("~/.lunarclient/launcher-cache")
    t.collect("~/.lunarclient/logs")
    t.collect("~/.lunarclient/offline/*/logs")
    t.collect("~/.lunarclient/offline/files/*/logs")

# Deletes Wget logs
if check_exists("~/wget-log"):
    t.msg("Deleting Wget log and hosts file...")
    t.collect("~/wget-log")
    t.collect("~/.wget-hsts")

# Deletes Cacher logs / I dunno either
if check_exists("~/.cacher"):
    t.msg("Deleting Cacher logs...")
    t.collect("~/.cacher/logs")

# Deletes Android (studio?) cache
if check_exists("~/.android"):
    t.msg("Deleting Android cache...")
    t.collect("~/.android/cache")

# Clears Gradle caches
if check_exists("~/.gradle"):
    t.msg("Clearing Gradle caches...")
    t.collect("~/.gradle/caches")

# Deletes Kite Autocomplete logs
if check_exists("~/.kite"):
    t.msg("Deleting Kite logs...")
    t.collect("~/.kite/logs")

if cmd("type 'brew'"):
    t.msg("Cleaning up Homebrew Cache...")
    if args.update:
        console.print("Updating Homebrew Recipes and upgrading...")
        t.collect("brew update && brew upgrade", command=True)
    t.collect(cmd("brew --cache"))

if cmd("type 'gem'"):  # TODO add count_dry
    t.msg("Cleaning up any old versions of gems")
    t.collect("gem mac_cleanup", command=True)

if cmd("type 'docker'"):  # TODO add count_dry
    t.msg("Cleaning up Docker")
    if not cmd("docker ps >/dev/null 2>&1"):
        t.collect("open --background -a Docker", command=True)
    t.collect("docker system prune -af", command=True)

if getenv("PYENV_VIRTUALENV_CACHE_PATH"):
    t.msg("Removing Pyenv-VirtualEnv Cache...")
    t.collect(getenv("PYENV_VIRTUALENV_CACHE_PATH"))

if cmd("type 'npm'"):
    t.msg("Cleaning up npm cache...")
    t.collect("npm cache clean --force", command=True)
    # For dry_run
    t.collect("~/.npm/*", dry=True)

if cmd("type 'yarn'"):
    t.msg("Cleaning up Yarn Cache...")
    t.collect("yarn cache clean --force", command=True)
    # For dry_run
    t.collect("~/Library/Caches/yarn", dry=True)

if cmd("type 'pod'"):
    t.msg("Cleaning up Pod Cache...")
    t.collect("pod cache clean --all", command=True)
    # For dry_run
    t.collect("~/Library/Caches/CocoaPods", dry=True)

if cmd("type 'go'"):
    t.msg("Clearing Go module cache...")
    t.collect("go clean -modcache", command=True)
    # For dry_run
    if getenv("GOPATH"):
        t.collect(f"{getenv('GOPATH')}/pkg/mod", dry=True)
    else:
        t.collect("~/go/pkg/mod", dry=True)

# Deletes all Microsoft Teams Caches and resets it to default - can fix also some performance issues
if check_exists("~/Library/Application Support/Microsoft/Teams"):
    t.msg("Deleting Microsoft Teams logs and caches...")
    t.collect("~/Library/Application Support/Microsoft/Teams/IndexedDB")
    t.collect("~/Library/Application Support/Microsoft/Teams/Cache")
    t.collect("~/Library/Application Support/Microsoft/Teams/Application Cache")
    t.collect("~/Library/Application Support/Microsoft/Teams/Code Cache")
    t.collect("~/Library/Application Support/Microsoft/Teams/blob_storage")
    t.collect("~/Library/Application Support/Microsoft/Teams/databases")
    t.collect("~/Library/Application Support/Microsoft/Teams/gpucache")
    t.collect("~/Library/Application Support/Microsoft/Teams/Local Storage")
    t.collect("~/Library/Application Support/Microsoft/Teams/tmp")
    t.collect("~/Library/Application Support/Microsoft/Teams/*logs*.txt")
    t.collect("~/Library/Application Support/Microsoft/Teams/watchdog")
    t.collect("~/Library/Application Support/Microsoft/Teams/*watchdog*.json")

# Deletes Poetry cache
if cmd("type 'poetry'") or check_exists("~/Library/Caches/pypoetry"):
    t.msg("Deleting Poetry cache...")
    t.collect("~/Library/Caches/pypoetry")

# Removes Java heap dumps
t.msg("Deleting Java heap dumps...")
t.collect("~/*.hprof")

t.msg("Cleaning up DNS cache...")
t.collect("sudo dscacheutil -flushcache", command=True)
t.collect("sudo killall -HUP mDNSResponder", command=True)

t.msg("Purging inactive memory...")
t.collect("sudo purge", command=True)


@catch_exception
def main() -> None:
    def count_free_space():
        return int(cmd("df / | tail -1 | awk '{print $4}'"))

    def cleanup():
        oldAvailable = count_free_space()

        for item in t.execute_list:
            if not item.get("msg"):
                continue

            for task in track(item["query"], description=item["msg"], transient=True, total=len(item["query"])):
                if task.startswith("cmd_"):
                    task = task[4:]
                else:
                    task = f'sudo rm -rf "{task}"'
                cmd(task)

        for brew_task in track(
                ["brew mac_cleanup -s", "brew tap --repair"],
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
