# mac-cleanup-py

[![PyPI](https://img.shields.io/pypi/v/mac_cleanup)](https://pypi.org/project/mac-cleanup/)
[![Tests](https://github.com/mac-cleanup/mac-cleanup-py/actions/workflows/tox.yml/badge.svg)](https://github.com/mac-cleanup/mac-cleanup-py/actions/workflows/tox.yml)
[![CodeQL](https://github.com/mac-cleanup/mac-cleanup-py/actions/workflows/codeql.yml/badge.svg)](https://github.com/mac-cleanup/mac-cleanup-py/actions/workflows/codeql.yml)

## 🧹 Python cleanup script for macOS

**mac-cleanup-py** is a powerful cleanup script for macOS.\
This project is a rewrite of the original [mac-cleanup-sh](https://github.com/mac-cleanup/mac-cleanup-sh) rewritten in Python. 


## 🚀 Features

**mac-cleanup-py** helps you:

1. Empty Trash 
2. Delete unnecessary logs & files 
3. Clear cache

![mac-cleanup-demo](https://user-images.githubusercontent.com/44712637/231780851-d2197255-e24e-46ba-8355-42bcf588376d.gif)

<details>
   <summary>
   📦 Default Modules
   </summary>

  </br>

  - `adobe` - Clears **Adobe** cache files
  - `android` - Clears **Android** caches
  - `brew` - Clears **Homebrew** cache
  - `cacher` - Clears **Cacher** logs
  - `chrome` - Clears **Google Chrome** cache
  - `composer` - Clears **composer** cache
  - `dns_cache` - Clears **DNS** cache
  - `docker` - Cleanup dangling **Docker** Images and stopped containers
  - `dropbox` - Clears **Dropbox** cache
  - `gem` - Cleanup any old versions of **Gems**
  - `go` - Clears **Go** cache
  - `google_drive` - Clears **Google Drive** caches
  - `gradle` - Clears **Gradle** caches
  - `inactive_memory` - Purge **Inactive Memory**
  - `ios_apps` - Cleanup **iOS Applications**
  - `ios_backups` - Removes **iOS Device Backups**
  - `java_cache` - Removes **Java head dumps** from home directory
  - `jetbrains` - Removes logs from **PhpStorm**, **PyCharm** etc
  - `kite` - Deletes **Kite** logs
  - `lunarclient` - Removes **Lunar Client** logs and cache
  - `microsoft_teams` - Remove **Microsoft Teams** logs and cache
  - `minecraft` - Remove **Minecraft** logs and cache
  - `npm` - Cleanup **npm** Cache
  - `pnpm` - Cleanup **pnpm** Cache
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



## 📥 Installation

### Using Homebrew

```bash
brew tap mac-cleanup/mac-cleanup-py
brew install mac-cleanup-py
```

### Using pip

```bash
pip3 install mac-cleanup
```

## 🗑️ Uninstallation

### Using Homebrew

```bash
brew uninstall mac-cleanup-py
brew untap mac-cleanup/mac-cleanup-py
```

### Using pip

```bash
pip3 uninstall mac-cleanup
```

## 💡 Usage Options

Help menu:

```
$ mac-cleanup -h

usage: mac-cleanup [-h] [-n] [-u] [-c] [-p]

    A Mac Cleanup Utility in Python
    3.0.3
    https://github.com/mac-cleanup/mac-cleanup-py    

options:
  -h, --help         show this help message and exit
  -n, --dry-run      Dry run without deleting stuff
  -u, --update       Update HomeBrew on cleanup
  -c, --configure    Configure default and custom modules
  -p, --custom-path  Specify path for custom modules

```


## 🌟 Contributing
Contributions are always welcome!\
If you have any ideas, suggestions, or bug reports, feel free to submit an issue or open a pull request.

## 📝 License
This project is licensed under the [Apache-2.0 License](https://github.com/mac-cleanup/mac-cleanup-py/blob/main/LICENSE).
