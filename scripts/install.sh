#!/usr/bin/env bash
# scripts/install.sh — install shae-file-organizer
# Symlinks src/main.py into ~/.local/bin/shae-file-organizer.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_DIR/src/main.py"
TARGET="$HOME/.local/bin/shae-file-organizer"

mkdir -p "$HOME/.local/bin"

ln -sf "$SRC" "$TARGET"
chmod +x "$SRC"

echo "Installed shae-file-organizer -> $TARGET"
echo "Ensure $HOME/.local/bin is on your PATH, then run:"
echo "  shae-file-organizer organize ~/Downloads"
echo "  shae-file-organizer list ~/Downloads"
echo "  shae-file-organizer undo"
