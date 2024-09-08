# mac-cleanup-py

[![PyPI](https://img.shields.io/pypi/v/mac_cleanup)](https://pypi.org/project/mac-cleanup/)
[![Tests](https://github.com/mac-cleanup/mac-cleanup-py/actions/workflows/tox.yml/badge.svg)](https://github.com/mac-cleanup/mac-cleanup-py/actions/workflows/tox.yml)
[![CodeQL](https://github.com/mac-cleanup/mac-cleanup-py/actions/workflows/codeql.yml/badge.svg)](https://github.com/mac-cleanup/mac-cleanup-py/actions/workflows/codeql.yml)
[![JetBrains](https://img.shields.io/badge/Thanks-JetBrains-green.svg)](https://www.jetbrains.com)

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
- `bun` - Clears **Bun** cache
- `cacher` - Clears **Cacher** logs
- `chrome` - Clears **Google Chrome** cache
- `chromium` - Clears **Chromium** cache files
- `composer` - Clears **composer** cache
- `conan` - Clears **Conan** cache
- `docker` - Cleanup dangling **Docker** Images and stopped containers
- `dns_cache` - Clears **DNS** cache
- `dropbox` - Clears **Dropbox** cache
- `ea` - Clears **EA App** cache files
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
- `minecraft` - Remove **Minecraft** logs and cache
- `microsoft_teams` - Remove **Microsoft Teams** logs and cache
- `npm` - Cleanup **npm** Cache
- `obsidian` - Clears **Obsidian** cache files
- `nuget` - Clears **.nuget** package files
- `pnpm` - Cleanup **pnpm** Cache
- `pod` - Cleanup **CocoaPods** Cache Files
- `poetry` - Clears **Poetry** cache
- `pyenv` - Cleanup **Pyenv-VirtualEnv** Cache
- `steam` - Remove **Steam** logs and cache
- `system_caches` - Clear **System cache**
- `system_log` - Clear **System Log** Files
- `telegram` - Clear old **Telegram** Cache
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
usage: mac-cleanup [-h] [-n] [-u] [-c] [-p] [-f]

    Python cleanup script for macOS
    Version: 3.1.0
    https://github.com/mac-cleanup/mac-cleanup-py

options:
  -h, --help         show this help message and exit
  -n, --dry-run      Run without deleting stuff
  -u, --update       Update Homebrew on cleanup
  -c, --configure    Open module configuration screen
  -p, --custom-path  Specify path for custom modules
  -f, --force        Accept all warnings

```

## 🌟 Contributing

Contributions are always welcome!\
If you have any ideas, suggestions, or bug reports, feel free to submit an issue or open a pull request.

## 📝 License

This project is licensed under the [Apache-2.0 License](https://github.com/mac-cleanup/mac-cleanup-py/blob/main/LICENSE).

## 👏 Acknowledgements

This project is developed using tools provided by the _JetBrains OSS Development Program_.

> Find out more about their program and how they support open source [here](https://jb.gg/OpenSourceSupport).

<a href="https://www.jetbrains.com">
  <img src="https://resources.jetbrains.com/storage/products/company/brand/logos/jb_square.svg" alt="JetBrains" width="80">
</a>
