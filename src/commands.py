import os, zlib
from .gfxdata import GfxData
from .modelincc import write_model_inc_c
from .geoincc import write_geo_inc_c
from .anims import write_animations, write_animation_table


def usage(exit_code):
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


def error(error_message: str):
    print(f"\n\033[0;31mError: {error_message}\033[0m")
    usage(1)


def is_compressed(data: bytes):
    return data[:8].decode() == "DYNOSBIN"


def get_dest_filepath(filepath: str, ext_from: str, ext_to: str):
    i = filepath.rfind(ext_from)
    j = filepath.rfind("/")
    return (filepath[:i] if i != -1 and i > j else filepath) + ext_to


def compress(filepath: str, data: bytes):
    if is_compressed(data):
        error(f"File `{filepath}` is already compressed")

    bin_data = zlib.compress(data)
    bin_filepath = get_dest_filepath(filepath, ".raw", ".bin")
    with open(bin_filepath, "wb") as f:
        f.write(b"DYNOSBIN")
        f.write(len(data).to_bytes(8, byteorder="little", signed=False))
        f.write(bin_data)
        print(f"`{filepath}` -> `{bin_filepath}`")
    return bin_data, bin_filepath


def decompress(filepath: str, data: bytes):
    if not is_compressed(data):
        error(f"File `{filepath}` is already decompressed")

    raw_data = zlib.decompress(data[16:])
    raw_filepath = get_dest_filepath(filepath, ".bin", ".raw")
    with open(raw_filepath, "wb") as f:
        f.write(raw_data)
        print(f"`{filepath}` -> `{raw_filepath}`")
    return raw_data, raw_filepath


def extract(filepath: str, data: bytes):
    if is_compressed(data):
        data, _ = decompress(filepath, data)

    print()
    gfxdata = GfxData.read(data)

    dirpath = get_dest_filepath(filepath, ".", "")
    model_name = dirpath.split("/")[-1]

    print("")
    print("--------------------------------")
    print("model:", model_name)
    print("lights1:", len(gfxdata.lights1))
    print("textures:", len(gfxdata.textures))
    print("vertices:", len(gfxdata.vertices))
    print("displaylists:", len(gfxdata.displaylists))
    print("geolayouts:", len(gfxdata.geolayouts))
    print("animations:", len(gfxdata.animations))
    print("priority: %02X" % (gfxdata.priority))
    print("--------------------------------")

    os.makedirs(dirpath, exist_ok=True)
    write_model_inc_c(dirpath, model_name, gfxdata)
    write_geo_inc_c(dirpath, gfxdata)
    write_animations(dirpath, gfxdata)
    write_animation_table(dirpath, gfxdata)


OPTIONS_TO_COMMANDS = {
    "-c": compress,
    "-d": decompress,
    "-e": extract,
}
