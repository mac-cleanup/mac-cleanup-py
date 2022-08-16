from . import *

t = Collector()


def trash():
    t.msg("Emptying the Trash 🗑 on all mounted volumes and the main HDD")
    t.collect("/Volumes/*/.Trashes/*")
    t.collect("~/.Trash/*")


def system_caches():
    t.msg("Clearing System Cache Files")
    t.collect("/Library/Caches/*")
    t.collect("/System/Library/Caches/*")
    t.collect("~/Library/Caches/*")
    t.collect("/private/var/folders/bh/*/*/*/*")


def system_log():
    t.msg("Clearing System Log Files")
    t.collect("/private/var/log/asl/*.asl")
    t.collect("/Library/Logs/DiagnosticReports/*")
    t.collect("/Library/Logs/CreativeCloud/*")
    t.collect("/Library/Logs/Adobe/*")
    t.collect("/Library/Logs/adobegc.log")
    t.collect("~/Library/Containers/com.apple.mail/Data/Library/Logs/Mail/*")
    t.collect("~/Library/Logs/CoreSimulator/*")


def jetbrains():
    from .utils import check_exists

    if check_exists("~/Library/Logs/JetBrains/"):
        t.msg("Clearing all application log files from JetBrains")
        t.collect("~/Library/Logs/JetBrains/*/")


def adobe():
    from .utils import check_exists

    if check_exists("~/Library/Application Support/Adobe/"):
        t.msg("Clearing Adobe Cache Files")
        t.collect("~/Library/Application Support/Adobe/Common/Media Cache Files/*")


def chrome():
    from .utils import check_exists

    if check_exists("~/Library/Application Support/Google/Chrome/"):
        t.msg("Clearing Google Chrome Cache Files")
        t.collect("~/Library/Application Support/Google/Chrome/Default/Application Cache/*")


def ios_apps():
    t.msg("Cleaning up iOS Applications")
    t.collect("~/Music/iTunes/iTunes Media/Mobile Applications/*")


def ios_backups():
    t.msg("Removing iOS Device Backups")
    t.collect("~/Library/Application Support/MobileSync/Backup/*")


def xcode():
    t.msg("Cleaning up XCode Derived Data and Archives")
    t.collect("~/Library/Developer/Xcode/DerivedData/*")
    t.collect("~/Library/Developer/Xcode/Archives/*")
    t.collect("~/Library/Developer/Xcode/iOS Device Logs/*")


def xcode_simulators():
    from .utils import cmd

    if cmd("type 'xcrun'"):
        t.msg("Cleaning up iOS Simulators")
        t.collect(
            "osascript -e 'tell application 'com.apple.CoreSimulator.CoreSimulatorService' to quit'",
            command=True
        )
        t.collect(
            "osascript -e 'tell application 'iOS Simulator' to quit'",
            command=True
        )
        t.collect(
            "osascript -e 'tell application 'Simulator' to quit'",
            command=True
        )
        t.collect(
            "xcrun simctl shutdown all",
            command=True
        )
        t.collect(
            "xcrun simctl erase all",
            command=True
        )
        # For dry_run
        t.collect(
            "~/Library/Developer/CoreSimulator/Devices/*/data/[!Library|var|tmp|Media]*",
            dry=True
        )
        t.collect(
            "/Users/wah/Library/Developer/CoreSimulator/Devices/*/data/Library/"
            "[!PreferencesCaches|Caches|AddressBook|Trial]*",
            dry=True
        )
        t.collect(
            "~/Library/Developer/CoreSimulator/Devices/*/data/Library/Caches/*",
            dry=True
        )
        t.collect(
            "~/Library/Developer/CoreSimulator/Devices/*/data/Library/AddressBook/AddressBook*",
            dry=True
        )


# Support deleting Dropbox Cache if they exist
def dropbox():
    from .utils import check_exists

    if check_exists("~/Dropbox"):
        t.msg("Clearing Dropbox 📦 Cache Files")
        t.collect("~/Dropbox/.dropbox.cache/*")


def google_drive():
    from .utils import check_exists

    if check_exists("~/Library/Application Support/Google/DriveFS/"):
        t.msg("Clearing Google Drive File Stream Cache Files")
        t.collect(
            "killall 'Google Drive File Stream'",
            command=True
        )
        t.collect("~/Library/Application Support/Google/DriveFS/[0-9a-zA-Z]*/content_cache")


def composer():
    from .utils import cmd

    if cmd("type 'composer'"):
        t.msg("Cleaning up composer")
        t.collect(
            "composer clearcache --no-interaction",
            command=True
        )
        # For dry_run
        t.collect(
            "~/Library/Caches/composer",
            dry=True
        )


# Deletes Steam caches, logs, and temp files
def steam():
    from .utils import check_exists

    if check_exists("~/Library/Application Support/Steam/"):
        t.msg("Clearing Steam Cache, Log, and Temp Files")
        t.collect("~/Library/Application Support/Steam/appcache")
        t.collect("~/Library/Application Support/Steam/depotcache")
        t.collect("~/Library/Application Support/Steam/logs")
        t.collect("~/Library/Application Support/Steam/steamapps/shadercache")
        t.collect("~/Library/Application Support/Steam/steamapps/temp")
        t.collect("~/Library/Application Support/Steam/steamapps/download")


# Deletes Minecraft logs
def minecraft():
    from .utils import check_exists

    if check_exists("~/Library/Application Support/minecraft"):
        t.msg("Clearing Minecraft Cache and Log Files")
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
def lunarclient():  # noqa
    from .utils import check_exists

    if check_exists("~/.lunarclient"):
        t.msg("Deleting Lunar Client logs and caches")
        t.collect("~/.lunarclient/game-cache")
        t.collect("~/.lunarclient/launcher-cache")
        t.collect("~/.lunarclient/logs")
        t.collect("~/.lunarclient/offline/*/logs")
        t.collect("~/.lunarclient/offline/files/*/logs")


# Deletes Wget logs
def wget_logs():
    from .utils import check_exists

    if check_exists("~/wget-log"):
        t.msg("Deleting Wget log and hosts file")
        t.collect("~/wget-log")
        t.collect("~/.wget-hsts")


# Deletes Cacher logs / I dunno either
def cacher():
    from .utils import check_exists

    if check_exists("~/.cacher"):
        t.msg("Deleting Cacher logs")
        t.collect("~/.cacher/logs")


# Deletes Android cache
def android():
    from .utils import check_exists

    if check_exists("~/.android"):
        t.msg("Deleting Android cache")
        t.collect("~/.android/cache")


# Clears Gradle caches
def gradle():
    from .utils import check_exists

    if check_exists("~/.gradle"):
        t.msg("Clearing Gradle caches")
        t.collect("~/.gradle/caches")


# Deletes Kite Autocomplete logs
def kite():
    from .utils import check_exists

    if check_exists("~/.kite"):
        t.msg("Deleting Kite logs")
        t.collect("~/.kite/logs")


def brew():
    from .utils import cmd

    if cmd("type 'brew'"):
        t.msg("Cleaning up Homebrew Cache")
        t.collect(
            "brew cleanup -s",
            command=True
        )
        t.collect(cmd("brew --cache"))
        t.collect(
            "brew tap --repair",
            command=True
        )
        if args.update:
            t.msg("Updating Homebrew Recipes and upgrading")
            t.collect(
                "brew update && brew upgrade",
                command=True
            )


def gem():
    from .utils import cmd

    if cmd("type 'gem'"):  # TODO add count_dry
        t.msg("Cleaning up any old versions of gems")
        t.collect(
            "gem cleanup",
            command=True
        )


def docker():
    from .utils import cmd

    if cmd("type 'docker'"):  # TODO add count_dry
        t.msg("Cleaning up Docker")
        if not cmd("docker ps >/dev/null 2>&1"):
            t.collect(
                "open --background -a Docker",
                command=True
            )
        t.collect(
            "docker system prune -af",
            command=True
        )


def pyenv():
    from os import getenv

    if getenv("PYENV_VIRTUALENV_CACHE_PATH"):
        t.msg("Removing Pyenv-VirtualEnv Cache")
        t.collect(getenv("PYENV_VIRTUALENV_CACHE_PATH"))


def npm():
    from .utils import cmd

    if cmd("type 'npm'"):
        t.msg("Cleaning up npm cache")
        t.collect(
            "npm cache clean --force",
            command=True
        )
        # For dry_run
        t.collect(
            "~/.npm/*",
            dry=True
        )


def yarn():
    from .utils import cmd

    if cmd("type 'yarn'"):
        t.msg("Cleaning up Yarn Cache")
        t.collect(
            "yarn cache clean --force",
            command=True
        )
        # For dry_run
        t.collect(
            "~/Library/Caches/yarn",
            dry=True
        )


def pod():
    from .utils import cmd

    if cmd("type 'pod'"):
        t.msg("Cleaning up Pod Cache")
        t.collect(
            "pod cache clean --all",
            command=True
        )
        # For dry_run
        t.collect(
            "~/Library/Caches/CocoaPods",
            dry=True
        )


def go():
    from .utils import cmd

    if cmd("type 'go'"):
        from os import getenv

        t.msg("Clearing Go module cache")
        t.collect(
            "go clean -modcache",
            command=True
        )
        # For dry_run
        if getenv("GOPATH"):
            t.collect(
                f"{getenv('GOPATH')}/pkg/mod",
                dry=True
            )
        else:
            t.collect(
                "~/go/pkg/mod",
                dry=True
            )


# Deletes all Microsoft Teams Caches and resets it to default - can fix also some performance issues
def microsoft_teams():
    from .utils import check_exists

    if check_exists("~/Library/Application Support/Microsoft/Teams"):
        t.msg("Deleting Microsoft Teams logs and caches")
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
def poetry():
    from .utils import cmd, check_exists

    if (
            cmd("type 'poetry'")
            or check_exists("~/Library/Caches/pypoetry")
    ):
        t.msg("Deleting Poetry cache")
        t.collect("~/Library/Caches/pypoetry")


# Removes Java heap dumps
def java_cache():
    t.msg("Deleting Java heap dumps")
    t.collect("~/*.hprof")


def dns_cache():
    t.msg("Cleaning up DNS cache")
    t.collect(
        "sudo dscacheutil -flushcache",
        command=True
    )
    t.collect(
        "sudo killall -HUP mDNSResponder",
        command=True
    )


def inactive_memory():
    t.msg("Purging inactive memory")
    t.collect(
        "sudo purge",
        command=True
    )
