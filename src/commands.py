# import os, zlib
# from . import prints
# from .gfxdata import GfxData
# from .modelincc import write_model_inc_c
# from .decomp.geoincc import write_geo_inc_c
# from .decomp.anims import write_animations, write_animation_table


# # TODO:
# # not used by the gui
# # broken, command line is unusable


# def is_compressed(data: bytes):
#     return data[:8].decode() == "DYNOSBIN"


# def get_dest_filepath(filepath: str, ext_from: str, ext_to: str|None = None):
#     i = filepath.rfind(ext_from)
#     j = filepath.rfind("/")
#     return (filepath[:i] if i != -1 and i > j else filepath) + (ext_to if ext_to is not None else ext_from)


# def compress(filepath: str, data: bytes):
#     if is_compressed(data):
#         prints.error(f"File `{filepath}` is already compressed")

#     bin_data = zlib.compress(data)
#     bin_filepath = get_dest_filepath(filepath, ".bin")
#     with open(bin_filepath, "wb") as f:
#         f.write(b"DYNOSBIN")
#         f.write(len(data).to_bytes(8, byteorder="little", signed=False))
#         f.write(bin_data)
#         prints.info(f"`{filepath}` -> `{bin_filepath}`")
#     return bin_data, bin_filepath


# def decompress(filepath: str, data: bytes):
#     if not is_compressed(data):
#         prints.error(f"File `{filepath}` is already decompressed")

#     raw_data = zlib.decompress(data[16:])
#     raw_filepath = get_dest_filepath(filepath, ".bin", ".bin.raw")
#     with open(raw_filepath, "wb") as f:
#         f.write(raw_data)
#         prints.info(f"`{filepath}` -> `{raw_filepath}`")
#     return raw_data, raw_filepath


# def extract(filepath: str, data: bytes):
#     if is_compressed(data):
#         data, _ = decompress(filepath, data)


# OPTIONS_TO_COMMANDS = {
#     "-c": compress,
#     "-d": decompress,
#     "-e": extract,
# }
