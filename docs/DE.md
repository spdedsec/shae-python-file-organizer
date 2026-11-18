# shae-python-file-organizer (de)

Ein dependencyfreies Python-CLI, das Dateien nach Erweiterung in Typ-Ordner
sortiert (Bilder, Dokumente, Audio, Video, Archive, Sonstiges) und `list`,
`undo` sowie einen optionalen polling-`watch`-Modus bietet.

## Installation

```bash
git clone https://github.com/spdedsec/shae-python-file-organizer.git
cd shae-python-file-organizer
bash scripts/install.sh
```

Dadurch wird `src/main.py` als `~/.local/bin/shae-file-organizer`
verlinkt. Stelle sicher, dass `~/.local/bin` in deinem `PATH` liegt.

## Verwendung

```bash
# Dateien nach Typ gruppiert anzeigen
shae-file-organizer list ~/Downloads

# Dateien in Typ-Ordner verschieben (Vorgang für undo aufzeichnen)
shae-file-organizer organize ~/Downloads

# Letzten organize-Vorgang rückgängig machen
shae-file-organizer undo

# Verzeichnis überwachen und neue Dateien automatisch sortieren (Strg+C zum Beenden)
shae-file-organizer watch ~/Downloads
```

## Befehle

| Befehl | Argument | Verhalten |
|--------|----------|-----------|
| `list` | `<dir>` | Dateien nach Typ-Ordner ausgeben |
| `organize` | `<dir>` | Dateien in `images/`, `docs/`, `audio/`, `video/`, `archives/`, `other/` verschieben |
| `undo` | — | Letzten organize-Vorgang über `.shae_organize_undo.json` rückgängig machen |
| `watch` | `<dir>` | Verzeichnis abfragen und neue Dateien automatisch sortieren |

## Lokale Prüfung

```bash
make test
```

Erstellt Beispieldateien in `/tmp/shae-organize-test` und führt
`list` → `organize` → `undo` → `list` aus, um das Round-Trip-Verhalten zu
prüfen.

## Anforderungen

- Python 3 (nur Standardbibliothek)

## Lizenz

MIT
