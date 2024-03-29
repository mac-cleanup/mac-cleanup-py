#! /bin/bash

# Check no version
if [[ -z "$1" ]]; then echo "No version supplied"; exit 1; fi

# Check incorrect version
if ! echo "$1" | grep -Eq '^[0-9]+\.[0-9]\.[0-9]+$'; then echo "Incorrect version"; exit 1; fi

# Get current version
currentVersion="$(grep -oE '(?:^version = \")(\d|\.)+(?:\")' pyproject.toml | sed -r 's/^version = "(([0-9]|\.)+)"/\1/g')"

# Replace in pyproject
sed -ri "" "s/^version = \"$currentVersion\"/version = \"$1\"/g" ./pyproject.toml

# Replace in README
sed -ri "" "s/$currentVersion/$1/g" ./README.md

exit 0
