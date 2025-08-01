import os, zlib
from . import prints
from .gfxdata import GfxData
from .write import geolayouts, displaylists, animations, behaviors


def is_compressed(data: bytes) -> bool:
    return data[:8].decode() == "DYNOSBIN"


def get_dest_filepath(filepath: str, ext_from: str, ext_to: str|None = None) -> str:
    i = filepath.rfind(ext_from)
    j = filepath.rfind("/")
    return (filepath[:i] if i != -1 and i > j else filepath) + (ext_to if ext_to is not None else ext_from)


def get_raw_data(filepath: str, create_dir: bool = False, ext: str|None = None) -> tuple[bytes, str]:
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
    if create_dir and ext is not None:
        dirpath = get_dest_filepath(filepath, ext, "")
        os.makedirs(dirpath, exist_ok=True)

        raw_filename = os.path.basename(get_dest_filepath(filepath, ext, ext+".raw"))
        raw_filepath = os.path.join(dirpath, raw_filename)
        with open(raw_filepath, "wb") as f: f.write(raw_data)

        bin_filename = os.path.basename(get_dest_filepath(filepath, ext))
        bin_filepath = os.path.join(dirpath, bin_filename)
        with open(bin_filepath, "wb") as f: f.write(bin_data)

        return raw_data, dirpath

    return raw_data, filepath


def decomp_actor(filepath: str):
    data, dirpath = get_raw_data(filepath, True, ".bin")
    model_name = dirpath.split("/")[-1]
    gfxdata = GfxData.read(data)

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

    gfxdata.write_model_inc_c(dirpath, model_name)
    gfxdata.write_geo_inc_c(dirpath)
    gfxdata.write_animations(dirpath)
    gfxdata.write_animation_table(dirpath)
    prints.info("")
    prints.info(f"\033[0;32mModel files extracted successfully to `{dirpath}`\033[0m")
    prints.info("")


def decomp_texture(filepath: str):
    data, _ = get_raw_data(filepath)
    gfxdata = GfxData.read(data)
    texture_name, texture = next(iter(gfxdata.textures.items()))
    png_filepath = os.path.join(os.path.dirname(filepath), texture_name+".png")

    prints.info("")
    prints.info("--------------------------------")
    prints.info(f"texture: {texture_name}")
    prints.info("--------------------------------")
    prints.info("")

    texture.write(png_filepath)
    prints.info("")
    prints.info(f"\033[0;32mTexture file extracted successfully to `{png_filepath}`\033[0m")
    prints.info("")


def decomp_behavior(filepath: str):
    data, _ = get_raw_data(filepath, False)
    gfxdata = GfxData.read(data)
    dirpath = get_dest_filepath(filepath, ".bhv", "")
    os.makedirs(dirpath, exist_ok=True)
    behavior_data_filepath = os.path.join(dirpath, "behavior_data.c")

    prints.info("")
    prints.info("--------------------------------")
    prints.info(f"behaviors: {list(gfxdata.behaviors.keys())}")
    prints.info("--------------------------------")
    prints.info("")

    # write_behavior_data_c(behavior_data_filepath, gfxdata)
    prints.info("")
    prints.info(f"\033[0;32mBehavior files extracted successfully to `{dirpath}`\033[0m")
    prints.info("")


DECOMP_TABLE = {
    ".bin": {
        "name": "DynOS actor files",
        "compressed": True,
        "decomp": decomp_actor
    },
    ".tex": {
        "name": "DynOS texture files",
        "compressed": False,
        "decomp": decomp_texture
    },
    ".bhv": {
        "name": "DynOS behavior files",
        "compressed": False,
        "decomp": decomp_behavior
    }
}

