#!/bin/sh

RELEASE_VERSION="v0.0.1-beta"
REPO_URL="https://github.com/0x15BA88FF/devault/releases/download/${RELEASE_VERSION}/devault"
DESTINATION="/usr/bin/devault"

echo "Downloading release version $RELEASE_VERSION directly to $DESTINATION..."
if ! sudo curl -L -o "$DESTINATION" "$REPO_URL"; then
    echo "Failed to download the release."
    exit 1
fi

echo "Making the binary executable..."
if ! sudo chmod +x "$DESTINATION"; then
    echo "Failed to set executable permissions."
    exit 1
fi

echo "Installation completed successfully! Happy hacking"
