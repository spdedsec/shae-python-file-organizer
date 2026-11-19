#!/usr/bin/env python3
"""
SHAE Python File Organizer
Production-grade file organization CLI with undo support.
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# File type categories
CATEGORIES = {
    'images': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico', '.heic'},
    'documents': {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.tex', '.md', '.csv', '.xlsx', '.pptx'},
    'audio': {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.opus'},
    'video': {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg'},
    'archives': {'.zip', '.tar', '.gz', '.bz2', '.xz', '.7z', '.rar', '.tar.gz', '.tar.xz'},
    'code': {'.py', '.js', '.ts', '.html', '.css', '.json', '.xml', '.yaml', '.yml', '.sh', '.rs', '.go', '.java', '.cpp', '.c', '.h'},
    'executables': {'.exe', '.msi', '.deb', '.rpm', '.dmg', '.pkg', '.appimage', '.bin', '.run'},
    'fonts': {'.ttf', '.otf', '.woff', '.woff2', '.eot'},
    'data': {'.db', '.sqlite', '.sql', '.parquet', '.feather', '.h5', '.hdf5'},
}

UNDO_FILE = '.shae_organize_undo.json'

def get_category(ext: str) -> str:
    ext = ext.lower()
    for cat, extensions in CATEGORIES.items():
        if ext in extensions:
            return cat
    return 'other'

def organize_directory(target_dir: Path, dry_run: bool = False) -> Dict:
    """Organize files in target directory by category."""
    if not target_dir.exists():
        raise FileNotFoundError(f"Directory not found: {target_dir}")
    if not target_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {target_dir}")
    
    undo_data = {
        'timestamp': datetime.now().isoformat(),
        'directory': str(target_dir.resolve()),
        'moves': []
    }
    
    stats = {cat: 0 for cat in CATEGORIES}
    stats['other'] = 0
    stats['skipped'] = 0
    
    for file_path in target_dir.iterdir():
        if not file_path.is_file():
            continue
        if file_path.name.startswith('.'):
            stats['skipped'] += 1
            continue
        if file_path.name == UNDO_FILE:
            stats['skipped'] += 1
            continue
        
        category = get_category(file_path.suffix)
        dest_dir = target_dir / category
        
        if not dry_run:
            dest_dir.mkdir(exist_ok=True)
            dest_path = dest_dir / file_path.name
            
            # Handle name conflicts
            counter = 1
            original_dest = dest_path
            while dest_path.exists():
                stem = original_dest.stem
                suffix = original_dest.suffix
                dest_path = dest_dir / f"{stem} ({counter}){suffix}"
                counter += 1
            
            shutil.move(str(file_path), str(dest_path))
            undo_data['moves'].append({
                'src': str(dest_path),
                'dst': str(file_path)
            })
        
        stats[category] += 1
    
    if not dry_run and undo_data['moves']:
        undo_path = target_dir / UNDO_FILE
        with open(undo_path, 'w') as f:
            json.dump(undo_data, f, indent=2)
    
    return stats

def undo_organize(target_dir: Path) -> int:
    """Undo the last organize operation."""
    undo_path = target_dir / UNDO_FILE
    if not undo_path.exists():
        raise FileNotFoundError("No undo data found. Nothing to undo.")
    
    with open(undo_path) as f:
        undo_data = json.load(f)
    
    if undo_data['directory'] != str(target_dir.resolve()):
        raise ValueError("Undo data is for a different directory.")
    
    restored = 0
    for move in reversed(undo_data['moves']):
        src = Path(move['src'])
        dst = Path(move['dst'])
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            restored += 1
    
    undo_path.unlink()
    return restored

def list_files(target_dir: Path) -> Dict:
    """List files grouped by category."""
    if not target_dir.exists():
        raise FileNotFoundError(f"Directory not found: {target_dir}")
    
    grouped = {cat: [] for cat in CATEGORIES}
    grouped['other'] = []
    
    for file_path in target_dir.iterdir():
        if not file_path.is_file() or file_path.name.startswith('.'):
            continue
        category = get_category(file_path.suffix)
        grouped[category].append(file_path.name)
    
    return {k: v for k, v in grouped.items() if v}

def print_stats(stats: Dict, dry_run: bool = False):
    prefix = "[DRY RUN] " if dry_run else ""
    print(f"\n{prefix}Organization complete:")
    total = 0
    for cat, count in stats.items():
        if count > 0:
            print(f"  {cat:12} : {count}")
            total += count
    print(f"  {'total':12} : {total}")

def main():
    parser = argparse.ArgumentParser(
        prog='shae-file-organizer',
        description='SHAE File Organizer - Organize files by type with undo support',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  shae-file-organizer organize ~/Downloads
  shae-file-organizer organize ~/Downloads --dry-run
  shae-file-organizer list ~/Downloads
  shae-file-organizer undo ~/Downloads
        """
    )
    parser.add_argument('command', choices=['organize', 'list', 'undo'], help='Command to execute')
    parser.add_argument('directory', nargs='?', default='.', help='Target directory (default: current)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    
    args = parser.parse_args()
    target_dir = Path(args.directory).resolve()
    
    try:
        if args.command == 'organize':
            stats = organize_directory(target_dir, dry_run=args.dry_run)
            print_stats(stats, args.dry_run)
        elif args.command == 'list':
            grouped = list_files(target_dir)
            for cat, files in grouped.items():
                print(f"\n{cat.upper()} ({len(files)}):")
                for f in sorted(files):
                    print(f"  {f}")
        elif args.command == 'undo':
            restored = undo_organize(target_dir)
            print(f"Restored {restored} file(s).")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
