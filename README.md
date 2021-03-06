# mac-cleanup-py

### 👨‍💻 Python cleanup script for macOS 

#### [mac-cleanup-sh](https://github.com/mac-cleanup/mac-cleanup-sh) rewritten in Python


### What does script do?

1. Cleans Trash
2. Deletes unnecessary logs & files
3. Removes cache

![macCleanupPy](https://user-images.githubusercontent.com/44712637/177019329-d0d40ac4-256d-4332-ac06-41ec54327d8e.gif)

<details>
   <summary>
   Full functionality
   </summary>

  * Empty the Trash on All Mounted Volumes and the Main HDD
  * Clear System Log Files
  * Clear Adobe Cache Files
  * Cleanup iOS Applications
  * Remove iOS Device Backups
  * Cleanup Xcode Derived Data and Archives
  * Reset iOS simulators
  * Cleanup Homebrew Cache
  * Cleanup Any Old Versions of Gems
  * Cleanup Dangling Docker Images
  * Purge Inactive Memory
  * Cleanup pip cache
  * Cleanup Pyenv-VirtualEnv Cache
  * Cleanup npm Cache
  * Cleanup Yarn Cache
  * Cleanup Docker Images and Stopped Containers
  * Cleanup CocoaPods Cache Files
  * Cleanup composer cache
  * Cleanup Dropbox cache
  * Remove PhpStorm logs
  * Remove Minecraft logs and cache
  * Remove Steam logs and cache
  * Remove Lunar Client logs and cache
  * Remove Microsoft Teams logs and cache
  * Remove Wget logs and hosts
  * Removes Cacher logs
  * Deletes Android caches
  * Clears Gradle caches
  * Deletes Kite logs
  * Clears Go module cache
  * Clears Poetry cache

</details>



## Install Automatically

### Using homebrew

```bash
brew tap mac-cleanup/mac-cleanup-py
brew install mac-cleanup-py
```

### Using curl

```bash
python3 <(curl -fsSL https://raw.githubusercontent.com/mac-cleanup/mac-cleanup-py/main/install) --install
```

### Using wget

```bash
python3 <(wget https://raw.githubusercontent.com/mac-cleanup/mac-cleanup-py/main/install -O -) --install
```

## Uninstall

### Using curl

```bash
python3 <(curl -fsSL https://raw.githubusercontent.com/mac-cleanup/mac-cleanup-py/main/install) --uninstall
```

### Using wget

```bash
python3 <(wget https://raw.githubusercontent.com/mac-cleanup/mac-cleanup-py/main/install -O -)  --uninstall
```

## Usage Options

Help menu:

```
$ mac-cleanup -h

usage: mac-cleanup [-h] [-d] [-u]

    A Mac Cleanup Utility in Python
    https://github.com/mac-cleanup/mac-cleanup-py


options:
  -h, --help     show this help message and exit
  -d, --dry-run  Shows approx space to be cleaned
  -u, --update   Script will update brew while cleaning
```
