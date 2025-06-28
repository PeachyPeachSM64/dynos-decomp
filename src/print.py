def usage(exit_code: int):
    print("\033[0;33m", end="")
    print(r"""
  ______  ___  _  __  ____
  \   \ \/ / \| |/  \/ __/
   | D \  /| \\ | () \__ \
  /___//_/ |_|\_|\__/____/
        D E C O M P
""")
    print("\033[0m", end="")
    print("""
Usage: \033[0;36mpython dynos-decomp.py \033[0;35m[OPTION] \033[0;34m[FILE]\033[0m
Compress, decompress or decompile a DynOS binary \033[0;34mFILE\033[0m.

If no \033[0;35mOPTION\033[0m provided, compress or decompile \033[0;34mFILE\033[0m.

Options:
  \033[0;35m-c\033[0m  compress \033[0;34mFILE\033[0m if not already compressed
  \033[0;35m-d\033[0m  decompress \033[0;34mFILE\033[0m if not already decompressed
  \033[0;35m-e\033[0m  extract source files (geo, model, textures...) from \033[0;34mFILE\033[0m

Examples:
  python dynos-decomp.py -d mario_geo.bin    decompress `mario_geo.bin` into `mario_geo.raw`
  python dynos-decomp.py -c mario_geo.raw    compress `mario_geo.raw` into `mario_geo.bin`
  python dynos-decomp.py -e mario_geo.bin    extract files from `mario_geo.bin` into a `mario_geo` directory
""")
    exit(exit_code)


def info(message: str, *args, **kwargs):
    print(message, *args, **kwargs)


def warning(message: str):
    print(f"\033[0;33mWarning: {message}\033[0m")


def error(message: str):
    print(f"\033[0;31mError: {message}\033[0m")
    usage(1)
