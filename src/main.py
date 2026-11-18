#!/usr/bin/env python3
"""SHAE File Organizer — CLI tool for sorting files into type folders.

Commands:
    organize <dir>   sort files into type folders by extension
    list <dir>       list files grouped by type
    undo             revert last organize operation (writes .shae_organize_undo.json)
    watch <dir>      poll a directory and auto-sort new files (stdlib only)

Designed per the SHAE field manual: precise over decorative, flat and physical,
type does the work. No dependencies beyond the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Extension -> folder mapping (lowercase, no leading dot)
# ---------------------------------------------------------------------------
EXTENSION_MAP = {
    # images
    "jpg": "images", "jpeg": "images", "png": "images", "gif": "images",
    "bmp": "images", "svg": "images", "webp": "images", "ico": "images",
    "tiff": "images", "tif": "images",
    # documents
    "pdf": "docs", "doc": "docs", "docx": "docs", "txt": "docs",
    "rtf": "docs", "odt": "docs", "xls": "docs", "xlsx": "docs",
    "ppt": "docs", "pptx": "docs", "csv": "docs", "md": "docs",
    # audio
    "mp3": "audio", "wav": "audio", "flac": "audio", "aac": "audio",
    "ogg": "audio", "wma": "audio",
    # video
    "mp4": "video", "avi": "video", "mkv": "video", "mov": "video",
    "wmv": "video", "flv": "video", "webm": "video",
    # archives
    "zip": "archives", "tar": "archives", "gz": "archives", "rar": "archives",
    "7z": "archives", "bz2": "archives", "xz": "archives",
}

TYPE_FOLDERS = ("images", "docs", "audio", "video", "archives", "other")

UNDO_FILENAME = ".shae_organize_undo.json"


def type_for_extension(ext: str) -> str:
    """Return the type folder for a file extension (defaults to 'other')."""
    return EXTENSION_MAP.get(ext.lower(), "other")


def classify(path: Path) -> str:
    """Classify a path into a type folder. Directories classify as 'other'."""
    if path.is_dir() or path.name.startswith("."):
        return "other"
    return type_for_extension(path.suffix.lstrip("."))


def list_files(root: Path) -> dict[str, list[Path]]:
    """Group regular (non-hidden) files in root by type folder.

    Hidden files (such as the undo journal) are skipped so they are never
    listed or moved by this tool.
    """
    grouped: dict[str, list[Path]] = {t: [] for t in TYPE_FOLDERS}
    for entry in sorted(root.iterdir()):
        if entry.is_file() and not entry.name.startswith("."):
            grouped[classify(entry)].append(entry)
    return grouped


def load_undo(root: Path) -> list[dict[str, str]]:
    """Load the recorded move operations from the undo file."""
    undo_file = root / UNDO_FILENAME
    if not undo_file.exists():
        return []
    try:
        with undo_file.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_undo(root: Path, operations: list[dict[str, str]]) -> None:
    """Persist move operations so they can be reverted with `undo`."""
    undo_file = root / UNDO_FILENAME
    with undo_file.open("w", encoding="utf-8") as fh:
        json.dump(operations, fh, indent=2)


def unique_destination(dest: Path) -> Path:
    """Return a non-clobbering destination by appending (1), (2), ..."""
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    i = 1
    while dest.exists():
        dest = dest.parent / f"{stem} ({i}){suffix}"
        i += 1
    return dest


def organize(root: Path) -> int:
    """Move files in root into type folders and record the operation."""
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 1

    grouped = list_files(root)
    operations: list[dict[str, str]] = []
    moved = 0

    for folder in TYPE_FOLDERS:
        files = grouped[folder]
        if not files:
            continue
        target_dir = root / folder
        target_dir.mkdir(exist_ok=True)
        for src in files:
            dest = unique_destination(target_dir / src.name)
            shutil.move(str(src), str(dest))
            operations.append({"source": str(src), "destination": str(dest)})
            moved += 1

    save_undo(root, operations)
    used = sum(1 for files in grouped.values() if files)
    print(f"organized {moved} file(s) into {used} folder(s)")
    return 0


def undo(root: Path) -> int:
    """Revert the last organize operation recorded in root."""
    operations = load_undo(root)
    if not operations:
        print("nothing to undo")
        return 0

    restored = 0
    for op in reversed(operations):
        src = Path(op["destination"])
        dest = unique_destination(Path(op["source"]))
        if not src.exists():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))
        restored += 1

    undo_file = root / UNDO_FILENAME
    if undo_file.exists():
        undo_file.unlink()
    print(f"reverted {restored} file(s)")
    return 0


def watch(root: Path, interval: float = 2.0) -> int:
    """Poll root and auto-sort newly created files until interrupted."""
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 1

    print(f"watching {root} (Ctrl+C to stop)...")
    seen: set[Path] = set()
    try:
        while True:
            for entry in root.iterdir():
                if entry.is_file() and entry not in seen:
                    seen.add(entry)
                    folder = classify(entry)
                    target_dir = root / folder
                    target_dir.mkdir(exist_ok=True)
                    dest = unique_destination(target_dir / entry.name)
                    shutil.move(str(entry), str(dest))
                    print(f"moved {entry.name} -> {folder}/")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nstopped watching")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shae-file-organizer",
        description="Sort files into type folders by extension.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_organize = sub.add_parser("organize", help="sort files into type folders")
    p_organize.add_argument("dir", help="directory to organize")

    p_list = sub.add_parser("list", help="list files grouped by type")
    p_list.add_argument("dir", help="directory to list")

    p_undo = sub.add_parser("undo", help="revert last organize operation")
    p_undo.add_argument("dir", nargs="?", default=".", help="directory to revert (default: current directory)")

    p_watch = sub.add_parser("watch", help="poll directory and auto-sort new files")
    p_watch.add_argument("dir", help="directory to watch")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "organize":
        return organize(Path(args.dir))
    if args.command == "list":
        grouped = list_files(Path(args.dir))
        for folder in TYPE_FOLDERS:
            files = grouped[folder]
            print(f"\n{folder.upper()}")
            if not files:
                print("  (none)")
                continue
            for f in files:
                print(f"  {f.name}")
        return 0
    if args.command == "undo":
        return undo(Path(args.dir))
    if args.command == "watch":
        return watch(Path(args.dir))

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
