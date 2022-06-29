#!usr/bin/env python3

from os import remove, getenv
from os.path import expanduser, exists
from glob import glob

from math import floor, log, pow

from subprocess import Popen, PIPE

from argparse import ArgumentParser, RawTextHelpFormatter

parser = ArgumentParser(
    description=
    """
A Mac Cleanup Utility in Python
https://github.com/Drugsosos/mac-cleanup-py
""",
    formatter_class=RawTextHelpFormatter,
)

parser.add_argument('-d', '--dry-run', help='Shows approx space to be cleaned',
                    action='store_true')
parser.add_argument('-u', '--update', help="Script will update brew while cleaning",
                    action='store_true')

args = parser.parse_args()

args.dry_run = True

path_list = list()

home = expanduser("~")


def cmd(
        command: str,
) -> str:
    return Popen(command, shell=True, stdout=PIPE).communicate()[0].strip().decode('utf-8')


def check_exists(
        path: str,
) -> bool:
    if path[0] == '~':
        result = exists(home + path)
    else:
        result = exists(path)
    return result


def bytes_to_human(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(floor(log(size_bytes, 1024)))
    p = pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def collect_paths(
        path: str,
) -> None:
    if not path:
        return
    if path[0] == '~':
        path_list.extend(glob(home + path[1:]))
    else:
        path_list.extend(glob(path))


def remove_paths(
) -> None:
    if not args.dry_run:
        [remove(path) for path in path_list]
        path_list.clear()


def get_dir_size(
        path: str,
):
    import os

    total_size = 0
    for dir_path, dir_names, filenames in os.walk(path):
        for filename in filenames:
            tmp_size = os.path.getsize(os.path.join(dir_path, filename))
            total_size += tmp_size
    return total_size


def count_dry():
    return sum([get_dir_size(path) for path in path_list])


oldAvailable = int(cmd('df / | tail -1 | awk \'{print $4}\''))

collect_paths('/Volumes/*/.Trashes/*')
collect_paths('~/.Trash/*')
print('Emptying the Trash 🗑 on all mounted volumes and the main HDD...')
remove_paths()

collect_paths('/Library/Caches/*')
collect_paths('/System/Library/Caches/*')
collect_paths('~/Library/Caches/*')
collect_paths('/private/var/folders/bh/*/*/*/*')
print('Clearing System Cache Files...')
remove_paths()

collect_paths('/private/var/log/asl/*.asl')
collect_paths('/Library/Logs/DiagnosticReports/*')
collect_paths('/Library/Logs/CreativeCloud/*')
collect_paths('/Library/Logs/Adobe/*')
collect_paths('/Library/Logs/adobegc.log')
collect_paths('~/Library/Containers/com.apple.mail/Data/Library/Logs/Mail/*')
collect_paths('~/Library/Logs/CoreSimulator/*')
print('Clearing System Log Files...')
remove_paths()

if check_exists('~/Library/Logs/JetBrains/'):
    collect_paths('~/Library/Logs/JetBrains/*/')
    print('Clearing all application log files from JetBrains...')
    remove_paths()

if check_exists('~/Library/Application\ Support/Adobe/'):
    collect_paths('~/Library/Application\ Support/Adobe/Common/Media\ Cache\ Files/*')
    print('Clearing Adobe Cache Files...')
    remove_paths()

if check_exists('~/Library/Application\ Support/Google/Chrome/'):
    collect_paths('~/Library/Application\ Support/Google/Chrome/Default/Application\ Cache/*')
    print('Clearing Google Chrome Cache Files...')
    remove_paths()

collect_paths('~/Music/iTunes/iTunes\ Media/Mobile\ Applications/*')
print('Cleaning up iOS Applications...')
remove_paths()

collect_paths('~/Library/Application\ Support/MobileSync/Backup/*')
print('Removing iOS Device Backups...')
remove_paths()

collect_paths('~/Library/Developer/Xcode/DerivedData/*')
collect_paths('~/Library/Developer/Xcode/Archives/*')
collect_paths('~/Library/Developer/Xcode/iOS Device Logs/*')
print('Cleaning up XCode Derived Data and Archives...')
remove_paths()

if cmd('type "xcrun"'):
    if not args.dry_run:
        print('Cleaning up iOS Simulators...')
        cmd('osascript -e \'tell application "com.apple.CoreSimulator.CoreSimulatorService" to quit\'')
        cmd('osascript -e \'tell application "iOS Simulator" to quit\'')
        cmd('osascript -e \'tell application "Simulator" to quit\'')
        cmd('xcrun simctl shutdown all')
        cmd('xcrun simctl erase all')
    else:
        collect_paths('~/Library/Developer/CoreSimulator/Devices/*/data/[!Library|var|tmp|Media]*')
        collect_paths(
            '/Users/wah/Library/Developer/CoreSimulator/Devices/*/data/Library/[!PreferencesCaches|Caches|AddressBook]*'
        )
        collect_paths('~/Library/Developer/CoreSimulator/Devices/*/data/Library/Caches/*')
        collect_paths('~/Library/Developer/CoreSimulator/Devices/*/data/Library/AddressBook/AddressBook*')
        print(path_list)

# Support deleting Dropbox Cache if they exist
if check_exists('"/Users/${HOST}/Dropbox"'):
    collect_paths('~/Dropbox/.dropbox.cache/*')
    print('Clearing Dropbox 📦 Cache Files...')
    remove_paths()

if check_exists('~/Library/Application\ Support/Google/DriveFS/'):
    collect_paths('~/Library/Application\ Support/Google/DriveFS/[0-9a-zA-Z]*/content_cache')
    print('Clearing Google Drive File Stream Cache Files...')
    cmd('killall "Google Drive File Stream"')
    remove_paths()

if cmd('type "composer"'):
    if not args.dry_run:
        print('Cleaning up composer...')
        cmd('composer clearcache --no-interaction')
    else:
        collect_paths('~/Library/Caches/composer')

# Deletes Steam caches, logs, and temp files
# -Astro
if check_exists('~/Library/Application\ Support/Steam/'):
    collect_paths('~/Library/Application\ Support/Steam/appcache')
    collect_paths('~/Library/Application\ Support/Steam/depotcache')
    collect_paths('~/Library/Application\ Support/Steam/logs')
    collect_paths('~/Library/Application\ Support/Steam/steamapps/shadercache')
    collect_paths('~/Library/Application\ Support/Steam/steamapps/temp')
    collect_paths('~/Library/Application\ Support/Steam/steamapps/download')
    print('Clearing Steam Cache, Log, and Temp Files...')
    remove_paths()

# Deletes Minecraft logs
# -Astro
if check_exists('~/Library/Application\ Support/minecraft'):
    collect_paths('~/Library/Application\ Support/minecraft/logs')
    collect_paths('~/Library/Application\ Support/minecraft/crash-reports')
    collect_paths('~/Library/Application\ Support/minecraft/webcache')
    collect_paths('~/Library/Application\ Support/minecraft/webcache2')
    collect_paths('~/Library/Application\ Support/minecraft/crash-reports')
    collect_paths('~/Library/Application\ Support/minecraft/*.log')
    collect_paths('~/Library/Application\ Support/minecraft/launcher_cef_log.txt')
    if check_exists('~/Library/Application\ Support/minecraft/.mixin.out'):
        collect_paths('~/Library/Application\ Support/minecraft/.mixin.out')
    print('Clearing Minecraft Cache and Log Files...')
    remove_paths()

# Deletes Lunar Client logs (Minecraft alternate client)
# -Astro
if check_exists('~/.lunarclient'):
    collect_paths('~/.lunarclient/game-cache')
    collect_paths('~/.lunarclient/launcher-cache')
    collect_paths('~/.lunarclient/logs')
    collect_paths('~/.lunarclient/offline/*/logs')
    collect_paths('~/.lunarclient/offline/files/*/logs')
    print('Deleting Lunar Client logs and caches...')
    remove_paths()

# Deletes Wget logs
# -Astro
if check_exists('~/wget-log'):
    collect_paths('~/wget-log')
    collect_paths('~/.wget-hsts')
    print('Deleting Wget log and hosts file...')
    remove_paths()

# Deletes Cacher logs
# I dunno either
# -Astro
if check_exists('~/.cacher'):
    collect_paths('~/.cacher/logs')
    print('Deleting Cacher logs...')
    remove_paths()

# Deletes Android (studio?) cache
# -Astro
if check_exists('~/.android'):
    collect_paths('~/.android/cache')
    print('Deleting Android cache...')
    remove_paths()

# Clears Gradle caches
# -Astro
if check_exists('~/.gradle'):
    collect_paths('~/.gradle/caches')
    print('Clearing Gradle caches...')
    remove_paths()

# Deletes Kite Autocomplete logs
# -Astro
if check_exists('~/.kite'):
    collect_paths('~/.kite/logs')
    print('Deleting Kite logs...')
    remove_paths()

if cmd('type "brew"'):
    if args.update:
        print('Updating Homebrew Recipes...')
        cmd('brew update')
        print('Upgrading and removing outdated formulae...')
        cmd('brew upgrade')
    collect_paths(cmd('brew --cache)"'))
    print('Cleaning up Homebrew Cache...')
    if not args.dry_run:
        cmd('brew cleanup -s')
        remove_paths()
        cmd('brew tap --repair')
    else:
        remove_paths()

if cmd('type "gem"'):  # TODO add count_dry
    if not args.dry_run:
        print('Cleaning up any old versions of gems')
        cmd('gem cleanup')

if cmd('type "docker"'):  # TODO add count_dry
    if not args.dry_run:
        if not cmd('docker ps >/dev/null 2>&1'):
            cmd('open --background -a Docker')
        print('Cleaning up Docker')
        cmd('docker system prune -af')

if getenv('PYENV_VIRTUALENV_CACHE_PATH'):
    collect_paths('"$PYENV_VIRTUALENV_CACHE_PATH"')
    print('Removing Pyenv-VirtualEnv Cache...')
    remove_paths()

if cmd('type "npm"'):
    if not args.dry_run:
        print('Cleaning up npm cache...')
        cmd('npm cache clean --force')
    else:
        collect_paths('~/.npm/*')

if cmd('type "yarn"'):
    if not args.dry_run:
        print('Cleaning up Yarn Cache...')
        cmd('yarn cache clean --force')
    else:
        collect_paths('~/Library/Caches/yarn')

if cmd('type "pod"'):
    if not args.dry_run:
        print('Cleaning up Pod Cache...')
        cmd('pod cache clean --all')
    else:
        collect_paths('~/Library/Caches/CocoaPods')

if cmd('type "go"'):
    if not args.dry_run:
        print('Clearing Go module cache...')
        cmd('go clean -modcache')
    else:
        if getenv('GOPATH'):
            collect_paths(f'{getenv("GOPATH")}/pkg/mod')
        else:
            collect_paths('~/go/pkg/mod')

# Deletes all Microsoft Teams Caches and resets it to default - can fix also some performance issues
# -Astro
if check_exists('~/Library/Application\ Support/Microsoft/Teams'):
    collect_paths('~/Library/Application\ Support/Microsoft/Teams/IndexedDB')
    collect_paths('~/Library/Application\ Support/Microsoft/Teams/Cache')
    collect_paths('~/Library/Application\ Support/Microsoft/Teams/Application\ Cache')
    collect_paths('~/Library/Application\ Support/Microsoft/Teams/Code\ Cache')
    collect_paths('~/Library/Application\ Support/Microsoft/Teams/blob_storage')
    collect_paths('~/Library/Application\ Support/Microsoft/Teams/databases')
    collect_paths('~/Library/Application\ Support/Microsoft/Teams/gpucache')
    collect_paths('~/Library/Application\ Support/Microsoft/Teams/Local\ Storage')
    collect_paths('~/Library/Application\ Support/Microsoft/Teams/tmp')
    collect_paths('~/Library/Application\ Support/Microsoft/Teams/*logs*.txt')
    collect_paths('~/Library/Application\ Support/Microsoft/Teams/watchdog')
    collect_paths('~/Library/Application\ Support/Microsoft/Teams/*watchdog*.json')
    print('Deleting Microsoft Teams logs and caches...')
    remove_paths()

# Deletes Poetry cache
if cmd('type "poetry"') or check_exists('~/Library/Caches/pypoetry'):
    collect_paths('~/Library/Caches/pypoetry')
    print('Deleting Poetry cache...')
    remove_paths()

# Removes Java heap dumps
collect_paths('~/*.hprof')
print('Deleting Java heap dumps...')
remove_paths()

if not args.dry_run:
    print('Cleaning up DNS cache...')
    cmd('sudo dscacheutil -flushcache')
    cmd('sudo killall -HUP mDNSResponder')

if not args.dry_run:
    print('Purging inactive memory...')
    cmd('sudo purge')

if not args.dry_run:
    print('Success')
    newAvailable = int(cmd('df / | tail -1 | awk \'{print $4}\''))
    print(bytes_to_human(newAvailable - oldAvailable))
else:
    print(bytes_to_human(count_dry()))

if __name__ == '__main__':
    pass
