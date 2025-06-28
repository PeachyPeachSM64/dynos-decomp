import os, zlib
from .print import info, error
from .gfxdata import GfxData
from .modelincc import write_model_inc_c
from .geoincc import write_geo_inc_c
from .anims import write_animations, write_animation_table


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
        info(f"`{filepath}` -> `{bin_filepath}`")
    return bin_data, bin_filepath


def decompress(filepath: str, data: bytes):
    if not is_compressed(data):
        error(f"File `{filepath}` is already decompressed")

    raw_data = zlib.decompress(data[16:])
    raw_filepath = get_dest_filepath(filepath, ".bin", ".raw")
    with open(raw_filepath, "wb") as f:
        f.write(raw_data)
        info(f"`{filepath}` -> `{raw_filepath}`")
    return raw_data, raw_filepath


def extract(filepath: str, data: bytes):
    if is_compressed(data):
        data, _ = decompress(filepath, data)

    info("")
    gfxdata = GfxData.read(data)

    dirpath = get_dest_filepath(filepath, ".", "")
    model_name = dirpath.split("/")[-1]

    info("")
    info("--------------------------------")
    info("model:", model_name)
    info("lights1:", len(gfxdata.lights1))
    info("textures:", len(gfxdata.textures))
    info("vertices:", len(gfxdata.vertices))
    info("displaylists:", len(gfxdata.displaylists))
    info("geolayouts:", len(gfxdata.geolayouts))
    info("animations:", len(gfxdata.animations))
    info("priority: %02X" % (gfxdata.priority))
    info("--------------------------------")
    info("")

    os.makedirs(dirpath, exist_ok=True)
    write_model_inc_c(dirpath, model_name, gfxdata)
    write_geo_inc_c(dirpath, gfxdata)
    write_animations(dirpath, gfxdata)
    write_animation_table(dirpath, gfxdata)
    info("")
    info(f"\033[0;32mModel files extracted successfully to `{dirpath}`\033[0m")


OPTIONS_TO_COMMANDS = {
    "-c": compress,
    "-d": decompress,
    "-e": extract,
}
