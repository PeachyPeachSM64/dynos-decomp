```
  ______  ___  _  __  ____
  \   \ \/ / \| |/  \/ __/
   | D \  /| \\ | () \__ \
  /___//_/ |_|\_|\__/____/
        D E C O M P
```

A Python script to decompile DynOS binary models.

## Installation

- Make sure Python is installed in your system (if not, go to https://www.python.org/downloads/)
- Clone or download this repository
- Open a terminal inside this cloned/downloaded repo
- Run `python dynos-decomp.py`

```
Usage: python dynos-decomp.py [OPTION] [FILE]
Compress, decompress or decompile a DynOS binary FILE.

If no OPTION provided, compress or decompile FILE.

Options:
  -c  compress FILE if not already compressed
  -d  decompress FILE if not already decompressed
  -e  extract source files (geo, model, textures...) from FILE

Examples:
  python dynos-decomp.py -d mario_geo.bin        decompress `mario_geo.bin` into `mario_geo.bin.raw`
  python dynos-decomp.py -c mario_geo.bin.raw    compress `mario_geo.bin.raw` into `mario_geo.bin`
  python dynos-decomp.py -e mario_geo.bin        extract files from `mario_geo.bin` into a `mario_geo` directory
```
