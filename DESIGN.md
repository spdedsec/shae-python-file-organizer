# DESIGN.md — shae-python-file-organizer

Design system applied per the SHAE field manual (`shared/design-system.md`).
This CLI has no UI layer, so the design system is expressed in its command
contract, output formatting, and documentation rather than pixels.

## Core principles

### Precise over decorative
Output is aligned, mono-spaced metadata with no ornamental noise. Commands do
one thing and report plainly: `list` groups files by type under uppercase
folder labels; `organize` reports a single count line; `undo` reports the
reverted count.

### Flat and physical
No animations, no spinners, no decorative borders in terminal output. Files
are moved (not copied) into real folders on disk — a physical, deterministic
operation. Zero-radius, 1px-border thinking maps to: no hidden state, no
fancy progress indicators, just the filesystem.

### Type does the work
Folder names are the interface: `IMAGES`, `DOCS`, `AUDIO`, `VIDEO`,
`ARCHIVES`, `OTHER`. Uppercase short labels per the design system. Extension
mapping is explicit and case-insensitive; unrecognized extensions fall through
to `other`.

### Confident restraint
One signal colour (oxide #B3341B) conceptually marks errors — printed to
stderr when a path is not a directory. Warm paper / ink palette is reflected
in the documentation (README, DESIGN.md) which uses the paper/ink/oxide
scheme in its HTML rendering.

## Accessibility

- Complete keyboard path: every command is invoked via keyboard arguments.
- Error messages go to stderr with non-zero exit codes.
- No colour-only information; all status is conveyed in text.

## Motion

Not applicable to a CLI (no UI transitions). If a future TUI is added, state
changes will use 140–240ms and reduced-motion fallbacks.

## Files

- `src/main.py` — argparse CLI; stdout for reports, stderr for errors.
- `scripts/install.sh` — symlinks to `~/.local/bin/shae-file-organizer`.
- `Makefile` — `make test` exercises list → organize → undo → list round trip.
- `docs/DE.md`, `docs/ES.md` — localized install guides.
