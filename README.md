# mac-cleanup-py

[![PyPI](https://img.shields.io/pypi/v/mac_cleanup)](https://pypi.org/project/mac-cleanup/)
[![Tests](https://github.com/mac-cleanup/mac-cleanup-py/actions/workflows/tox.yml/badge.svg)](https://github.com/mac-cleanup/mac-cleanup-py/actions/workflows/tox.yml)
[![CodeQL](https://github.com/mac-cleanup/mac-cleanup-py/actions/workflows/codeql.yml/badge.svg)](https://github.com/mac-cleanup/mac-cleanup-py/actions/workflows/codeql.yml)

### 👨‍💻 Python cleanup script for macOS 

#### [mac-cleanup-sh](https://github.com/mac-cleanup/mac-cleanup-sh) rewritten in Python


### What does script do?

1. Cleans Trash
2. Deletes unnecessary logs & files
3. Removes cache

![mac-cleanup_v2_X_X](https://user-images.githubusercontent.com/44712637/184389183-449cae99-4d40-4ca1-9523-1fb3dcf809dd.gif)

<details>
   <summary>
   Default modules
   </summary>

  </br>

  - `adobe` - Clears **Adobe** cache files
  - `android` - Clears **Android** caches
  - `brew` - Clears **Homebrew** cache
  - `cacher` - Clears **Cacher** logs
  - `chrome` - Clears Google Chrome cache
  - `composer` - Clears composer cache
  - `dns_cache` - Clears DNS cache
  - `docker` - Cleanup dangling **Docker Images** and stopped **containers**
  - `dropbox` - Clears **Dropbox** cache
  - `gem` - Cleanup any old versions of **Gems**
  - `go` - Clears **Go** cache
  - `google_drive` - Clears **Google Drive** caches
  - `gradle` - Clears **Gradle** caches
  - `inactive_memory` - Purge Inactive Memory
  - `ios_apps` - Cleanup **iOS Applications**
  - `ios_backups` - Removes **iOS Device Backups**
  - `java_cache` - Removes **Java head dumps** from home directory
  - `jetbrains` - Removes logs from **PhpStorm**, **PyCharm**  etc
  - `kite` - Deletes **Kite** logs
  - `lunarclient` - Removes **Lunar Client** logs and cache
  - `microsoft_teams` - Remove **Microsoft Teams** logs and cache
  - `minecraft` - Remove **Minecraft** logs and cache
  - `npm` - Cleanup **npm** Cache
  - `pod` - Cleanup **CocoaPods** Cache Files
  - `poetry` - Clears **Poetry** cache
  - `pyenv` - Cleanup **Pyenv-VirtualEnv** Cache
  - `steam` - Remove **Steam** logs and cache
  - `system_caches` - Clear **System cache**
  - `system_log` - Clear **System Log** Files
  - `trash` - Empty the **Trash** on All Mounted Volumes and the Main HDD
  - `wget_logs` - Remove **Wget** logs and hosts
  - `xcode` - Cleanup **Xcode Derived Data** and **Archives**
  - `xcode_simulators` - Reset **iOS simulators**
  - `yarn` - Cleanup **yarn** Cache


</details>



## Install Automatically

### Using homebrew

```bash
brew tap mac-cleanup/mac-cleanup-py
brew install mac-cleanup-py
```

### Using pip

```bash
pip3 install mac-cleanup
```

## Uninstall

### Using homebrew

```bash
brew uninstall mac-cleanup-py
brew untap mac-cleanup/mac-cleanup-py
```

### Using pip

```bash
pip3 uninstall mac-cleanup
```

## Usage Options

Help menu:

```
$ mac-cleanup -h

usage: mac-cleanup [-h] [-d] [-u] [-c] [-m]

    A Mac Cleanup Utility in Python
    v2.2.4
    https://github.com/mac-cleanup/mac-cleanup-py

optional arguments:
  -h, --help       show this help message and exit
  -d, --dry-run    Shows approx space to be cleaned
  -u, --update     Script will update brew while cleaning
  -c, --configure  Launch modules configuration
  -m, --modules    Specify custom modules' path
```
