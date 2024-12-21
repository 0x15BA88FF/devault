#!/bin/sh

if [ ! -f "/usr/bin/devault" ]; then
    echo "The tool is not installed."
    exit 0
fi

echo "Uninstalling the tool..."
if sudo rm /usr/bin/devault; then
    echo "Uninstallation completed successfully."
else
    echo "Failed to remove the binary."
    exit 1
fi
