import os, zlib
from . import prints
from .gfxdata import GfxData
from .modelincc import write_model_inc_c
from .geoincc import write_geo_inc_c
from .anims import write_animations, write_animation_table


def is_compressed(data: bytes):
    return data[:8].decode() == "DYNOSBIN"


def get_dest_filepath(filepath: str, ext_from: str, ext_to: str|None = None):
    i = filepath.rfind(ext_from)
    j = filepath.rfind("/")
    return (filepath[:i] if i != -1 and i > j else filepath) + (ext_to if ext_to is not None else ext_from)


def compress(filepath: str, data: bytes):
    if is_compressed(data):
        prints.error(f"File `{filepath}` is already compressed")

    bin_data = zlib.compress(data)
    bin_filepath = get_dest_filepath(filepath, ".bin")
    with open(bin_filepath, "wb") as f:
        f.write(b"DYNOSBIN")
        f.write(len(data).to_bytes(8, byteorder="little", signed=False))
        f.write(bin_data)
        prints.info(f"`{filepath}` -> `{bin_filepath}`")
    return bin_data, bin_filepath


def decompress(filepath: str, data: bytes):
    if not is_compressed(data):
        prints.error(f"File `{filepath}` is already decompressed")

    raw_data = zlib.decompress(data[16:])
    raw_filepath = get_dest_filepath(filepath, ".bin", ".bin.raw")
    with open(raw_filepath, "wb") as f:
        f.write(raw_data)
        prints.info(f"`{filepath}` -> `{raw_filepath}`")
    return raw_data, raw_filepath


def extract(filepath: str, data: bytes):
    if is_compressed(data):
        data, _ = decompress(filepath, data)

    prints.info("")
    gfxdata = GfxData.read(data)

    dirpath = get_dest_filepath(filepath, ".bin", "")
    model_name = dirpath.split("/")[-1]

    prints.info("")
    prints.info("--------------------------------")
    prints.info(f"model: {model_name}")
    prints.info(f"lights1: {len(gfxdata.lights1)}")
    prints.info(f"textures: {len(gfxdata.textures)}")
    prints.info(f"vertices: {len(gfxdata.vertices)}")
    prints.info(f"displaylists: {len(gfxdata.displaylists)}")
    prints.info(f"geolayouts: {len(gfxdata.geolayouts)}")
    prints.info(f"animations: {len(gfxdata.animations)}")
    prints.info("priority: %02X" % (gfxdata.priority))
    prints.info("--------------------------------")
    prints.info("")

    os.makedirs(dirpath, exist_ok=True)
    write_model_inc_c(dirpath, model_name, gfxdata)
    write_geo_inc_c(dirpath, gfxdata)
    write_animations(dirpath, gfxdata)
    write_animation_table(dirpath, gfxdata)
    prints.info("")
    prints.info(f"\033[0;32mModel files extracted successfully to `{dirpath}`\033[0m")
    prints.info("")


def gui_decomp(filepath: str):
    with open(filepath, "rb") as f:
        data = f.read()

    # Get bin and raw data
    if is_compressed(data):
        raw_data = zlib.decompress(data[16:])
        bin_data = data
    else:
        raw_data = data
        bin_data = b"DYNOSBIN" + len(data).to_bytes(8, byteorder="little", signed=False) + zlib.compress(data)

    # Make dest dir, write raw and bin files
    dirpath = get_dest_filepath(filepath, ".bin", "")
    os.makedirs(dirpath, exist_ok=True)

    raw_filename = os.path.basename(get_dest_filepath(filepath, ".bin", ".bin.raw"))
    raw_filepath = os.path.join(dirpath, raw_filename)
    with open(raw_filepath, "wb") as f: f.write(raw_data)

    bin_filename = os.path.basename(get_dest_filepath(filepath, ".bin"))
    bin_filepath = os.path.join(dirpath, bin_filename)
    with open(bin_filepath, "wb") as f: f.write(bin_data)

    # Extract files
    extract(filepath, raw_data)


OPTIONS_TO_COMMANDS = {
    "-c": compress,
    "-d": decompress,
    "-e": extract,
}
