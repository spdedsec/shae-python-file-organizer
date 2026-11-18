# shae-python-file-organizer (es)

Una CLI de Python sin dependencias que ordena archivos en carpetas por tipo
(imágenes, documentos, audio, video, archivos comprimidos, otros) según su
extensión, con los comandos `list`, `undo` y un modo `watch` opcional de
sondeo.

## Instalación

```bash
git clone https://github.com/spdedsec/shae-python-file-organizer.git
cd shae-python-file-organizer
bash scripts/install.sh
```

Esto crea un symlink de `src/main.py` a `~/.local/bin/shae-file-organizer`.
Asegúrese de que `~/.local/bin` esté en su `PATH`.

## Uso

```bash
# Mostrar archivos agrupados por tipo
shae-file-organizer list ~/Downloads

# Mover archivos a carpetas por tipo y registrar la operación para deshacer
shae-file-organizer organize ~/Downloads

# Revertir la última operación organize
shae-file-organizer undo

# Sondear un directorio y ordenar archivos nuevos automáticamente (Ctrl+C para detener)
shae-file-organizer watch ~/Downloads
```

## Comandos

| Comando | Argumento | Comportamiento |
|---------|-----------|----------------|
| `list` | `<dir>` | Imprimir archivos agrupados por tipo de carpeta |
| `organize` | `<dir>` | Mover archivos a `images/`, `docs/`, `audio/`, `video/`, `archives/`, `other/` |
| `undo` | — | Revertir el último `organize` usando `.shae_organize_undo.json` |
| `watch` | `<dir>` | Sondear y ordenar archivos nuevos hasta interrumpir |

## Pruebas locales

```bash
make test
```

Crea archivos de ejemplo en `/tmp/shae-organize-test` y ejecuta
`list` → `organize` → `undo` → `list` para verificar el comportamiento de
ida y vuelta.

## Requisitos

- Python 3 (solo biblioteca estándar)

## Licencia

MIT
