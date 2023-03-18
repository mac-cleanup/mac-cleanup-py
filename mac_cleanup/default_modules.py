from mac_cleanup import *

clc = Collector()


def trash():
    with clc as t:
        t.message("Emptying the Trash 🗑 on all mounted volumes and the main HDD")
        t.add(
            Path("/Volumes/*/.Trashes/*")
        )
        t.add(
            Path("~/.Trash/*")
        )


def system_caches():
    with clc as t:
        t.message("Clearing System Cache Files")
        t.add(
            Path("/Library/Caches/*")
        )
        t.add(
            Path("/System/Library/Caches/*")
        )
        t.add(
            Path("~/Library/Caches/*")
        )
        t.add(
            Path("/private/var/folders/bh/*/*/*/*")
        )


def system_log():
    with clc as t:
        t.message("Clearing System Log Files")
        t.add(
            Path("/private/var/log/asl/*.asl")
        )
        t.add(
            Path("/Library/Logs/DiagnosticReports/*")
        )
        t.add(
            Path("/Library/Logs/CreativeCloud/*")
        )
        t.add(
            Path("/Library/Logs/Adobe/*")
        )
        t.add(
            Path("/Library/Logs/adobegc.log")
        )
        t.add(
            Path("~/Library/Containers/com.apple.mail/Data/Library/Logs/Mail/*")
        )
        t.add(
            Path("~/Library/Logs/CoreSimulator/*")
        )


def jetbrains():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Library/Logs/JetBrains/"):
        with clc as t:
            t.message("Clearing all application log files from JetBrains")
            t.add(
                Path("~/Library/Logs/JetBrains/*/")
            )


def adobe():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Library/Application Support/Adobe/"):
        with clc as t:
            t.message("Clearing Adobe Cache Files")
            t.add(
                Path("~/Library/Application Support/Adobe/Common/Media Cache Files/*")
            )


def chrome():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Library/Application Support/Google/Chrome/"):
        with clc as t:
            t.message("Clearing Google Chrome Cache Files")
            t.add(
                Path("~/Library/Application Support/Google/Chrome/Default/Application Cache/*")
            )


def ios_apps():
    with clc as t:
        t.message("Cleaning up iOS Applications")
        t.add(
            Path("~/Music/iTunes/iTunes Media/Mobile Applications/*")
        )


def ios_backups():
    with clc as t:
        t.message("Removing iOS Device Backups")
        t.add(
            Path("~/Library/Application Support/MobileSync/Backup/*")
        )


def xcode():
    with clc as t:
        t.message("Cleaning up XCode Derived Data and Archives")
        t.add(
            Path("~/Library/Developer/Xcode/DerivedData/*")
        )
        t.add(
            Path("~/Library/Developer/Xcode/Archives/*")
        )
        t.add(
            Path("~/Library/Developer/Xcode/iOS Device Logs/*")
        )


def xcode_simulators():
    from mac_cleanup.utils import cmd

    if cmd("type 'xcrun'"):
        with clc as t:
            t.message("Cleaning up iOS Simulators")
            t.add(
                Command("osascript -e 'tell application 'com.apple.CoreSimulator.CoreSimulatorService' to quit'")
            )
            t.add(
                Command("osascript -e 'tell application 'iOS Simulator' to quit'")
            )
            t.add(
                Command("osascript -e 'tell application 'Simulator' to quit'")
            )
            t.add(
                Command("xcrun simctl shutdown all")
            )
            t.add(
                Command("xcrun simctl erase all")
            )

            t.add(
                Path("~/Library/Developer/CoreSimulator/Devices/*/data/[!Library|var|tmp|Media]*")
                .dry_run_only()
            )
            t.add(
                Path(
                    "/Users/wah/Library/Developer/CoreSimulator/Devices/*/data/Library/"
                    "[!PreferencesCaches|Caches|AddressBook|Trial]*"
                )
                .dry_run_only()
            )
            t.add(
                Path("~/Library/Developer/CoreSimulator/Devices/*/data/Library/Caches/*")
                .dry_run_only()
            )
            t.add(
                Path("~/Library/Developer/CoreSimulator/Devices/*/data/Library/AddressBook/AddressBook*")
                .dry_run_only()
            )


# Support deleting Dropbox Cache if they exist
def dropbox():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Dropbox"):
        with clc as t:
            t.message("Clearing Dropbox 📦 Cache Files")
            t.add(
                Path("~/Dropbox/.dropbox.cache/*")
            )


def google_drive():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Library/Application Support/Google/DriveFS/"):
        with clc as t:
            t.message("Clearing Google Drive File Stream Cache Files")
            t.add(
                Command("killall 'Google Drive File Stream'")
            )
            t.add(
                Path("~/Library/Application Support/Google/DriveFS/[0-9a-zA-Z]*/content_cache")
            )


def composer():
    from mac_cleanup.utils import cmd

    if cmd("type 'composer'"):
        with clc as t:
            t.message("Cleaning up composer")
            t.add(
                Command("composer clearcache --no-interaction")
            )
            t.add(
                Path("~/Library/Caches/composer")
                .dry_run_only()
            )


# Deletes Steam caches, logs, and temp files
def steam():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Library/Application Support/Steam/"):
        with clc as t:
            t.message("Clearing Steam Cache, Log, and Temp Files")
            t.add(
                Path("~/Library/Application Support/Steam/appcache")
            )
            t.add(
                Path("~/Library/Application Support/Steam/depotcache")
            )
            t.add(
                Path("~/Library/Application Support/Steam/logs")
            )
            t.add(
                Path("~/Library/Application Support/Steam/steamapps/shadercache")
            )
            t.add(
                Path("~/Library/Application Support/Steam/steamapps/temp")
            )
            t.add(
                Path("~/Library/Application Support/Steam/steamapps/download")
            )


# Deletes Minecraft logs
def minecraft():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Library/Application Support/minecraft"):
        with clc as t:
            t.message("Clearing Minecraft Cache and Log Files")
            t.add(
                Path("~/Library/Application Support/minecraft/logs")
            )
            t.add(
                Path("~/Library/Application Support/minecraft/crash-reports")
            )
            t.add(
                Path("~/Library/Application Support/minecraft/webcache")
            )
            t.add(
                Path("~/Library/Application Support/minecraft/webcache2")
            )
            t.add(
                Path("~/Library/Application Support/minecraft/crash-reports")
            )
            t.add(
                Path("~/Library/Application Support/minecraft/*.log")
            )
            t.add(
                Path("~/Library/Application Support/minecraft/launcher_cef_log.txt")
            )

            if check_exists("~/Library/Application Support/minecraft/.mixin.out"):
                t.add(
                    Path("~/Library/Application Support/minecraft/.mixin.out")
                )


# Deletes Lunar Client logs (Minecraft alternate client)
def lunarclient():  # noqa
    from mac_cleanup.utils import check_exists

    if check_exists("~/.lunarclient"):
        with clc as t:
            t.message("Deleting Lunar Client logs and caches")
            t.add(
                Path("~/.lunarclient/game-cache")
            )
            t.add(
                Path("~/.lunarclient/launcher-cache")
            )
            t.add(
                Path("~/.lunarclient/logs")
            )
            t.add(
                Path("~/.lunarclient/offline/*/logs")
            )
            t.add(
                Path("~/.lunarclient/offline/files/*/logs")
            )


# Deletes Wget logs
def wget_logs():
    from mac_cleanup.utils import check_exists

    if check_exists("~/wget-log"):
        with clc as t:
            t.message("Deleting Wget log and hosts file")
            t.add(
                Path("~/wget-log")
            )
            t.add(
                Path("~/.wget-hsts")
            )


# Deletes Cacher logs / I dunno either
def cacher():
    from mac_cleanup.utils import check_exists

    if check_exists("~/.cacher"):
        with clc as t:
            t.message("Deleting Cacher logs")
            t.add(
                Path("~/.cacher/logs")
            )


# Deletes Android cache
def android():
    from mac_cleanup.utils import check_exists

    if check_exists("~/.android"):
        with clc as t:
            t.message("Deleting Android cache")
            t.add(
                Path("~/.android/cache")
            )


# Clears Gradle caches
def gradle():
    from mac_cleanup.utils import check_exists

    if check_exists("~/.gradle"):
        with clc as t:
            t.message("Clearing Gradle caches")
            t.add(
                Path("~/.gradle/caches")
            )


# Deletes Kite Autocomplete logs
def kite():
    from mac_cleanup.utils import check_exists

    if check_exists("~/.kite"):
        with clc as t:
            t.message("Deleting Kite logs")
            t.add(
                Path("~/.kite/logs")
            )


def brew():
    from mac_cleanup.utils import cmd

    if cmd("type 'brew'"):
        with clc as t:
            t.message("Cleaning up Homebrew Cache")

            # Get brew path
            brew_cache_path = cmd("brew --cache")

            t.add(
                Command("brew cleanup -s")
            )
            t.add(
                Path(brew_cache_path)
            )
            t.add(
                Command("brew tap --repair")
            )

        if args.update:
            with clc as t:
                t.message("Updating Homebrew Recipes and upgrading")
                t.add(
                    Command("brew update && brew upgrade")
                )


def gem():
    from mac_cleanup.utils import cmd

    if cmd("type 'gem'"):  # TODO add count_dry
        with clc as t:
            t.message("Cleaning up any old versions of gems")
            t.add(
                Command("gem cleanup")
            )


def docker():
    from mac_cleanup.utils import cmd

    if cmd("type 'docker'"):  # TODO add count_dry
        with clc as t:
            t.message("Cleaning up Docker")

            if not cmd("docker ps >/dev/null 2>&1"):
                t.add(
                    Command("open --background -a Docker")
                )

            t.add(
                Command("docker system prune -af")
                .with_prompt(
                    """\
                    Stopped containers, dangling images, unused networks, volumes, and build cache will be deleted
                    Continue?\
                    """
                )
            )


def pyenv():
    from os import getenv

    if pyenv_path := getenv("PYENV_VIRTUALENV_CACHE_PATH"):
        with clc as t:
            t.message("Removing Pyenv-VirtualEnv Cache")
            t.add(
                Path(pyenv_path)
            )


def npm():
    from mac_cleanup.utils import cmd

    if cmd("type 'npm'"):
        with clc as t:
            t.message("Cleaning up npm cache")
            t.add(
                Command("npm cache clean --force")
            )
            t.add(
                Path("~/.npm/*")
                .dry_run_only()
            )


def yarn():
    from mac_cleanup.utils import cmd

    if cmd("type 'yarn'"):
        with clc as t:
            t.message("Cleaning up Yarn Cache")
            t.add(
                Command("yarn cache clean --force")
            )
            t.add(
                Path("~/Library/Caches/yarn")

                .dry_run_only()
            )


def pod():
    from mac_cleanup.utils import cmd

    if cmd("type 'pod'"):
        with clc as t:
            t.message("Cleaning up Pod Cache")
            t.add(
                Command("pod cache clean --all")
            )

            t.add(
                Path("~/Library/Caches/CocoaPods")
                .dry_run_only()
            )


def go():
    from mac_cleanup.utils import cmd

    if cmd("type 'go'"):
        from os import getenv

        with clc as t:
            t.message("Clearing Go module cache")
            t.add(
                Command("go clean -modcache")
            )

            if go_path := getenv("GOPATH"):
                t.add(
                    Path(go_path + "/pkg/mod")
                    .dry_run_only()
                )
            else:
                t.add(
                    Path("~/go/pkg/mod")
                    .dry_run_only()
                )


# Deletes all Microsoft Teams Caches and resets it to default - can fix also some performance issues
def microsoft_teams():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Library/Application Support/Microsoft/Teams"):
        with clc as t:
            t.message("Deleting Microsoft Teams logs and caches")
            t.add(
                Path("~/Library/Application Support/Microsoft/Teams/IndexedDB")
            )
            t.add(
                Path("~/Library/Application Support/Microsoft/Teams/Cache")
            )
            t.add(
                Path("~/Library/Application Support/Microsoft/Teams/Application Cache")
            )
            t.add(
                Path("~/Library/Application Support/Microsoft/Teams/Code Cache")
            )
            t.add(
                Path("~/Library/Application Support/Microsoft/Teams/blob_storage")
            )
            t.add(
                Path("~/Library/Application Support/Microsoft/Teams/databases")
            )
            t.add(
                Path("~/Library/Application Support/Microsoft/Teams/gpucache")
            )
            t.add(
                Path("~/Library/Application Support/Microsoft/Teams/Local Storage")
            )
            t.add(
                Path("~/Library/Application Support/Microsoft/Teams/tmp")
            )
            t.add(
                Path("~/Library/Application Support/Microsoft/Teams/*logs*.txt")
            )
            t.add(
                Path("~/Library/Application Support/Microsoft/Teams/watchdog")
            )
            t.add(
                Path("~/Library/Application Support/Microsoft/Teams/*watchdog*.json")
            )


# Deletes Poetry cache
def poetry():
    from mac_cleanup.utils import cmd, check_exists

    if (
            cmd("type 'poetry'")
            or check_exists("~/Library/Caches/pypoetry")
    ):
        with clc as t:
            t.message("Deleting Poetry cache")
            t.add(
                Path("~/Library/Caches/pypoetry")
            )


# Removes Java heap dumps
def java_cache():
    with clc as t:
        t.message("Deleting Java heap dumps")
        t.add(
            Path("~/*.hprof")
        )


def dns_cache():
    with clc as t:
        t.message("Cleaning up DNS cache")
        t.add(
            Command("sudo dscacheutil -flushcache")
        )
        t.add(
            Command("sudo killall -HUP mDNSResponder")
        )


def inactive_memory():
    with clc as t:
        t.message("Purging inactive memory")
        t.add(
            Command("sudo purge")
        )
