#!/usr/bin/env bash
set -euo pipefail
echo "Installing SHAE Python File Organizer"
echo "Usage: shae-file-organizer organize|list|undo <directory>"
echo "Installing to ~/.local/bin/shae-file-organizer..."
mkdir -p ~/.local/bin
cp src/main.py ~/.local/bin/shae-file-organizer
chmod +x ~/.local/bin/shae-file-organizer
echo "Done! Run 'shae-file-organizer --help' to get started."
