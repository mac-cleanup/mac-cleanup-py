from mac_cleanup.core import ProxyCollector as Collector
from mac_cleanup.core_modules import Command, Path
from mac_cleanup.parser import args

clc = Collector()


def trash():
    with clc as unit:
        unit.message("Emptying the Trash 🗑 on all mounted volumes and the main HDD")
        unit.add(Path("/Volumes/*/.Trashes/*"))
        unit.add(Path("~/.Trash/*"))


def system_caches():
    with clc as unit:
        unit.message("Clearing System Cache Files")
        unit.add(
            Path("~/Library/Caches/*").with_prompt(
                "ALL USER CACHE will be DELETED, including Poetry, Jetbrains, Cocoa, yarn, Composer etc.\n" "Continue?"
            )
        )
        unit.add(Path("/private/var/folders/bh/*/*/*/*"))


def system_log():
    with clc as unit:
        unit.message("Clearing System Log Files")
        unit.add(Path("/private/var/log/asl/*.asl"))
        unit.add(Path("/Library/Logs/DiagnosticReports/*"))
        unit.add(Path("/Library/Logs/CreativeCloud/*"))
        unit.add(Path("/Library/Logs/Adobe/*"))
        unit.add(Path("/Library/Logs/adobegc.log"))
        unit.add(Path("~/Library/Containers/com.apple.mail/Data/Library/Logs/Mail/*"))
        unit.add(Path("~/Library/Logs/CoreSimulator/*"))


def jetbrains():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Library/Logs/JetBrains/"):
        with clc as unit:
            unit.message("Clearing all application log files from JetBrains")
            unit.add(Path("~/Library/Logs/JetBrains/*/"))


def adobe():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Library/Application Support/Adobe/"):
        with clc as unit:
            unit.message("Clearing Adobe Cache Files")
            unit.add(Path("~/Library/Application Support/Adobe/Common/Media Cache Files/*"))


def chrome():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Library/Application Support/Google/Chrome/"):
        with clc as unit:
            unit.message("Clearing Google Chrome Cache Files")
            unit.add(Path("~/Library/Application Support/Google/Chrome/Default/Application Cache/*"))


def ios_apps():
    with clc as unit:
        unit.message("Cleaning up iOS Applications")
        unit.add(Path("~/Music/iTunes/iTunes Media/Mobile Applications/*"))


def ios_backups():
    with clc as unit:
        unit.message("Removing iOS Device Backups")
        unit.add(Path("~/Library/Application Support/MobileSync/Backup/*"))


def xcode():
    with clc as unit:
        unit.message("Cleaning up XCode Derived Data and Archives")
        unit.add(Path("~/Library/Developer/Xcode/DerivedData/*"))
        unit.add(Path("~/Library/Developer/Xcode/Archives/*"))
        unit.add(Path("~/Library/Developer/Xcode/iOS Device Logs/*"))


def xcode_simulators():
    from mac_cleanup.utils import cmd

    if cmd("type 'xcrun'"):
        with clc as unit:
            unit.message("Cleaning up iOS Simulators")
            unit.add(Command("osascript -e 'tell application 'com.apple.CoreSimulator.CoreSimulatorService' to quit'"))
            unit.add(Command("osascript -e 'tell application 'iOS Simulator' to quit'"))
            unit.add(Command("osascript -e 'tell application 'Simulator' to quit'"))
            unit.add(Command("xcrun simctl shutdown all"))
            unit.add(
                Command("xcrun simctl erase all").with_prompt("All Xcode simulators will be pruned.\n" "Continue?")
            )

            unit.add(Path("~/Library/Developer/CoreSimulator/Devices/*/data/[!Library|var|tmp|Media]*").dry_run_only())
            unit.add(
                Path(
                    "~/Library/Developer/CoreSimulator/Devices/*/data/Library/"
                    "[!PreferencesCaches|Caches|AddressBook|Trial]*"
                ).dry_run_only()
            )
            unit.add(Path("~/Library/Developer/CoreSimulator/Devices/*/data/Library/Caches/*").dry_run_only())
            unit.add(
                Path("~/Library/Developer/CoreSimulator/Devices/*/data/Library/AddressBook/AddressBook*").dry_run_only()
            )


# Support deleting Dropbox Cache if they exist
def dropbox():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Dropbox"):
        with clc as unit:
            unit.message("Clearing Dropbox 📦 Cache Files")
            unit.add(Path("~/Dropbox/.dropbox.cache/*"))


def google_drive():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Library/Application Support/Google/DriveFS/"):
        with clc as unit:
            unit.message("Clearing Google Drive File Stream Cache Files")
            unit.add(Command("killall 'Google Drive File Stream'"))
            unit.add(Path("~/Library/Application Support/Google/DriveFS/[0-9a-zA-Z]*/content_cache"))


def composer():
    from mac_cleanup.utils import cmd

    if cmd("type 'composer'"):
        with clc as unit:
            unit.message("Cleaning up composer")
            unit.add(Command("composer clearcache --no-interaction"))
            unit.add(Path("~/Library/Caches/composer").dry_run_only())


# Deletes Steam caches, logs, and temp files
def steam():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Library/Application Support/Steam/"):
        with clc as unit:
            unit.message("Clearing Steam Cache, Log, and Temp Files")
            unit.add(Path("~/Library/Application Support/Steam/appcache"))
            unit.add(Path("~/Library/Application Support/Steam/depotcache"))
            unit.add(Path("~/Library/Application Support/Steam/logs"))
            unit.add(Path("~/Library/Application Support/Steam/steamapps/shadercache"))
            unit.add(Path("~/Library/Application Support/Steam/steamapps/temp"))
            unit.add(Path("~/Library/Application Support/Steam/steamapps/download"))


# Deletes Minecraft logs
def minecraft():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Library/Application Support/minecraft"):
        with clc as unit:
            unit.message("Clearing Minecraft Cache and Log Files")
            unit.add(Path("~/Library/Application Support/minecraft/logs"))
            unit.add(Path("~/Library/Application Support/minecraft/crash-reports"))
            unit.add(Path("~/Library/Application Support/minecraft/webcache"))
            unit.add(Path("~/Library/Application Support/minecraft/webcache2"))
            unit.add(Path("~/Library/Application Support/minecraft/crash-reports"))
            unit.add(Path("~/Library/Application Support/minecraft/*.log"))
            unit.add(Path("~/Library/Application Support/minecraft/launcher_cef_log.txt"))
            unit.add(Path("~/Library/Application Support/minecraft/command_history.txt"))

            if check_exists("~/Library/Application Support/minecraft/.mixin.out"):
                unit.add(Path("~/Library/Application Support/minecraft/.mixin.out"))


# Deletes Lunar Client logs (Minecraft alternate client)
def lunarclient():  # noqa
    from mac_cleanup.utils import check_exists

    if check_exists("~/.lunarclient"):
        with clc as unit:
            unit.message("Deleting Lunar Client logs and caches")
            unit.add(Path("~/.lunarclient/game-cache"))
            unit.add(Path("~/.lunarclient/launcher-cache"))
            unit.add(Path("~/.lunarclient/logs"))
            unit.add(Path("~/.lunarclient/offline/*/logs"))
            unit.add(Path("~/.lunarclient/offline/files/*/logs"))


# Deletes Wget logs
def wget_logs():
    from mac_cleanup.utils import check_exists

    if check_exists("~/wget-log"):
        with clc as unit:
            unit.message("Deleting Wget log and hosts file")
            unit.add(Path("~/wget-log"))
            unit.add(Path("~/.wget-hsts"))


# Deletes Cacher logs / I dunno either
def cacher():
    from mac_cleanup.utils import check_exists

    if check_exists("~/.cacher"):
        with clc as unit:
            unit.message("Deleting Cacher logs")
            unit.add(Path("~/.cacher/logs"))


# Deletes Android cache
def android():
    from mac_cleanup.utils import check_exists

    if check_exists("~/.android"):
        with clc as unit:
            unit.message("Deleting Android cache")
            unit.add(Path("~/.android/cache"))


# Clears Gradle caches
def gradle():
    from mac_cleanup.utils import check_exists

    if check_exists("~/.gradle"):
        with clc as unit:
            unit.message("Clearing Gradle caches")
            unit.add(
                Path("~/.gradle/caches").with_prompt(
                    "Gradle cache will be removed. It is chunky and kinda long to reinstall.\n" "Continue?"
                )
            )


# Deletes Kite Autocomplete logs
def kite():
    from mac_cleanup.utils import check_exists

    if check_exists("~/.kite"):
        with clc as unit:
            unit.message("Deleting Kite logs")
            unit.add(Path("~/.kite/logs"))


def brew():
    from mac_cleanup.utils import cmd

    if cmd("type 'brew'"):
        with clc as unit:
            unit.message("Cleaning up Homebrew Cache")

            # Get brew path
            brew_cache_path = cmd("brew --cache")

            unit.add(Command("brew cleanup -s"))
            unit.add(Path(brew_cache_path))
            unit.add(Command("brew tap --repair"))

        if args.update:
            with clc as unit:
                unit.message("Updating Homebrew Recipes and upgrading")
                unit.add(Command("brew update && brew upgrade"))


def gem():
    from mac_cleanup.utils import cmd

    if cmd("type 'gem'"):  # TODO add count_dry
        with clc as unit:
            unit.message("Cleaning up any old versions of gems")
            unit.add(Command("gem cleanup"))


def docker():
    from mac_cleanup.utils import cmd

    if cmd("type 'docker'"):  # TODO add count_dry
        with clc as unit:
            unit.message("Cleaning up Docker")

            # Flag for turning Docker off
            close_docker = False

            if not cmd("docker ps >/dev/null 2>&1"):
                unit.add(Command("open -jga Docker"))

                close_docker = True

            unit.add(
                Command("docker system prune -af").with_prompt(
                    "Stopped containers, dangling images, unused networks, volumes, and build cache will be deleted.\n"
                    "Continue?"
                )
            )

            # Close Docker if it was opened by cleaner
            if close_docker:
                unit.add(Command("killall Docker"))


def pyenv():
    from os import getenv

    if pyenv_path := getenv("PYENV_VIRTUALENV_CACHE_PATH"):
        with clc as unit:
            unit.message("Removing Pyenv-VirtualEnv Cache")
            unit.add(Path(pyenv_path))


def npm():
    from mac_cleanup.utils import cmd

    if cmd("type 'npm'"):
        with clc as unit:
            unit.message("Cleaning up npm cache")
            unit.add(Command("npm cache clean --force"))
            unit.add(Path("~/.npm/*").dry_run_only())


def pnpm():
    from mac_cleanup.utils import cmd

    if cmd("type 'pnpm'"):
        with clc as unit:
            unit.message("Cleaning up pnpm Cache...")
            unit.add(Command("pnpm store prune &>/dev/null"))
            unit.add(Path("~/.pnpm-store/*").dry_run_only())


def yarn():
    from mac_cleanup.utils import cmd

    if cmd("type 'yarn'"):
        with clc as unit:
            unit.message("Cleaning up Yarn Cache")
            unit.add(Command("yarn cache clean --force"))
            unit.add(Path("~/Library/Caches/yarn").dry_run_only())


def bun():
    from mac_cleanup.utils import cmd

    if cmd("type 'bun'"):
        with clc as unit:
            unit.message("Cleaning up Bun Cache")
            unit.add(Command("bun pm cache rm"))
            unit.add(Path("~/.bun/install/cache").dry_run_only())


def pod():
    from mac_cleanup.utils import cmd

    if cmd("type 'pod'"):
        with clc as unit:
            unit.message("Cleaning up Pod Cache")
            unit.add(Command("pod cache clean --all"))

            unit.add(Path("~/Library/Caches/CocoaPods").dry_run_only())


def go():
    from mac_cleanup.utils import cmd

    if cmd("type 'go'"):
        from os import getenv

        with clc as unit:
            unit.message("Clearing Go module cache")
            unit.add(Command("go clean -modcache"))

            if go_path := getenv("GOPATH"):
                unit.add(Path(go_path + "/pkg/mod").dry_run_only())
            else:
                unit.add(Path("~/go/pkg/mod").dry_run_only())


# Deletes all Microsoft Teams Caches and resets it to default - can fix also some performance issues
def microsoft_teams():
    from mac_cleanup.utils import check_exists

    if check_exists("~/Library/Application Support/Microsoft/Teams"):
        with clc as unit:
            unit.message("Deleting Microsoft Teams logs and caches")
            unit.add(Path("~/Library/Application Support/Microsoft/Teams/IndexedDB"))
            unit.add(Path("~/Library/Application Support/Microsoft/Teams/Cache"))
            unit.add(Path("~/Library/Application Support/Microsoft/Teams/Application Cache"))
            unit.add(Path("~/Library/Application Support/Microsoft/Teams/Code Cache"))
            unit.add(Path("~/Library/Application Support/Microsoft/Teams/blob_storage"))
            unit.add(Path("~/Library/Application Support/Microsoft/Teams/databases"))
            unit.add(Path("~/Library/Application Support/Microsoft/Teams/gpucache"))
            unit.add(Path("~/Library/Application Support/Microsoft/Teams/Local Storage"))
            unit.add(Path("~/Library/Application Support/Microsoft/Teams/tmp"))
            unit.add(Path("~/Library/Application Support/Microsoft/Teams/*logs*.txt"))
            unit.add(Path("~/Library/Application Support/Microsoft/Teams/watchdog"))
            unit.add(Path("~/Library/Application Support/Microsoft/Teams/*watchdog*.json"))


# Deletes Poetry cache
def poetry():
    from mac_cleanup.utils import check_exists, cmd

    if cmd("type 'poetry'") or check_exists("~/Library/Caches/pypoetry"):
        with clc as unit:
            unit.message("Deleting Poetry cache")
            unit.add(
                Path("~/Library/Caches/pypoetry").with_prompt(
                    "All non-local Poetry venvs will be deleted.\n" "Continue?"
                )
            )


# Removes Java heap dumps
def java_cache():
    with clc as unit:
        unit.message("Deleting Java heap dumps")
        unit.add(Path("~/*.hprof").with_prompt("All heap dumps (.hprof) in HOME dir will be deleted.\n" "Continue?"))


def dns_cache():
    with clc as unit:
        unit.message("Cleaning up DNS cache")
        unit.add(Command("sudo dscacheutil -flushcache"))
        unit.add(Command("sudo killall -HUP mDNSResponder"))


def inactive_memory():
    with clc as unit:
        unit.message("Purging inactive memory")
        unit.add(Command("sudo purge"))


def telegram():
    from mac_cleanup.utils import cmd

    with clc as unit:
        unit.message("Clear old Telegram cache")

        reopen_telegram = False

        if cmd("ps aux | grep '[T]elegram'"):
            reopen_telegram = True
            unit.add(Command("killall -KILL Telegram"))

        unit.add(
            Path("~/Library/Group Containers/*.ru.keepcoder.Telegram/stable/account-*/postbox/db").with_prompt(
                "Telegram cache will be deleted. Once reopened, cache will be rebuild smaller. Continue?"
            )
        )

        if reopen_telegram:
            unit.add(Command("open /Applications/Telegram.app"))


def conan():
    with clc as unit:
        unit.message("Clearing conan cache")
        unit.add(Command("""conan remove "*" -c"""))
        unit.add(Path("~/.conan2/p/"))


def nuget_cache():
    with clc as unit:
        unit.message("Emptying the .nuget folder's content of the current user")
        unit.add(
            Path("~/.nuget/packages/").with_prompt(
                "Deleting nuget packages probably will cause a lot of files being redownloaded!\n" "Continue?"
            )
        )


def obsidian_caches():
    with clc as unit:
        unit.message("Deleting all cache folders of Obsidian")
        unit.add(Path("~/Library/Application Support/obsidian/Cache/"))
        unit.add(Path("~/Library/Application Support/obsidian/Code Cache/"))
        unit.add(Path("~/Library/Application Support/obsidian/DawnGraphiteCache/"))
        unit.add(Path("~/Library/Application Support/obsidian/DawnWebGPUCache/"))
        unit.add(Path("~/Library/Application Support/obsidian/DawnWebGPUCache/"))
        unit.add(Path("~/Library/Application Support/obsidian/*.log"))


def ea_caches():
    with clc as unit:
        unit.message("Deleting all cache folders of the EA App")
        unit.add(Path("~/Library/Application Support/Electronic Arts/EA app/IGOCache/"))
        unit.add(Path("~/Library/Application Support/Electronic Arts/EA app/Logs/"))
        unit.add(Path("~/Library/Application Support/Electronic Arts/EA app/OfflineCache/"))
        unit.add(Path("~/Library/Application Support/Electronic Arts/EA app/CEF/BrowserCache/EADesktop/Cache/"))
        unit.add(Path("~/Library/Application Support/Electronic Arts/EA app/CEF/BrowserCache/EADesktop/Code Cache/"))
        unit.add(Path("~/Library/Application Support/Electronic Arts/EA app/CEF/BrowserCache/EADesktop/DawnCache/"))
        unit.add(Path("~/Library/Application Support/Electronic Arts/EA app/CEF/BrowserCache/EADesktop/GPUCache/"))


def chromium_caches():
    with clc as unit:
        unit.message("Deleting all cache folders of Chromium")
        unit.add(Path("~/Library/Application Support/Chromium/GraphiteDawnCache/"))
        unit.add(Path("~/Library/Application Support/Chromium/GrShaderCache/"))
        unit.add(Path("~/Library/Application Support/Chromium/ShaderCache/"))
        unit.add(Path("~/Library/Application Support/Chromium/Default/DawnCache/"))
        unit.add(Path("~/Library/Application Support/Chromium/Default/GPUCache/"))
