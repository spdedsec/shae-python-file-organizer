# shae-python-file-organizer

A dependency-free Python CLI that sorts files into type folders (images, docs,
audio, video, archives, other) by extension, with `list`, `undo`, and an
optional polling `watch` mode.

Part of the SHAE Tier 2 series. Built per the SHAE field manual design system:
precise over decorative, flat and physical, type does the work.

## Install

```bash
git clone https://github.com/spdedsec/shae-python-file-organizer.git
cd shae-python-file-organizer
bash scripts/install.sh
```

This symlinks `src/main.py` to `~/.local/bin/shae-file-organizer`. Make sure
`~/.local/bin` is on your `PATH`.

## Usage

```bash
# Show files in a directory grouped by type
shae-file-organizer list ~/Downloads

# Move files into type folders and record the operation for undo
shae-file-organizer organize ~/Downloads

# Revert the last organize operation (restores files to their original spots)
shae-file-organizer undo

# Poll a directory and auto-sort newly created files (Ctrl+C to stop)
shae-file-organizer watch ~/Downloads
```

## Commands

| Command | Argument | Behavior |
|---------|----------|----------|
| `list` | `<dir>` | Print files grouped by type folder |
| `organize` | `<dir>` | Move files into `images/`, `docs/`, `audio/`, `video/`, `archives/`, `other/` |
| `undo` | — | Revert the last `organize` using `.shae_organize_undo.json` |
| `watch` | `<dir>` | Poll and auto-sort new files until interrupted |

## Type mapping

Extensions are matched case-insensitively. Anything unrecognized goes to
`other/`.

- images: jpg, jpeg, png, gif, bmp, svg, webp, ico, tiff, tif
- docs: pdf, doc, docx, txt, rtf, odt, xls, xlsx, ppt, pptx, csv, md
- audio: mp3, wav, flac, aac, ogg, wma
- video: mp4, avi, mkv, mov, wmv, flv, webm
- archives: zip, tar, gz, rar, 7z, bz2, xz

## Test locally

```bash
make test
```

Creates sample files in `/tmp/shae-organize-test`, runs `list`, `organize`,
`undo`, and `list` again to verify round-trip behaviour.

## Requirements

- Python 3 (standard library only)

## License

MIT
