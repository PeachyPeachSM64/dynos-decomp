import os, zlib
from . import prints
from .decomp import is_compressed, get_dest_filepath, DECOMP_TABLE


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

    original_length = int.from_bytes(data[8:16], byteorder="little", signed=False)
    raw_data = zlib.decompress(data[16:])

    if len(raw_data) != original_length:
        prints.warning(f"Decompressed data length mismatch: expected {original_length}, got {len(raw_data)}")

    raw_filepath = get_dest_filepath(filepath, ".bin", ".bin.raw")
    with open(raw_filepath, "wb") as f:
        f.write(raw_data)
        prints.info(f"`{filepath}` -> `{raw_filepath}`")
    return raw_data, raw_filepath


def extract(filepath: str, data: bytes):
    file_ext = os.path.splitext(filepath)[1].lower()

    if file_ext not in DECOMP_TABLE:
        prints.error(f"Unsupported file type: {file_ext}. Supported types: {list(DECOMP_TABLE.keys())}")

    file_info = DECOMP_TABLE[file_ext]

    if is_compressed(data) and not file_info["compressed"]:
        prints.info(f"Decompressing {filepath} first...")
        data, decompressed_path = decompress(filepath, data)
        filepath = decompressed_path

    file_info["decomp"](filepath)


OPTIONS_TO_COMMANDS = {
    "-c": compress,
    "-d": decompress,
    "-e": extract,
}
