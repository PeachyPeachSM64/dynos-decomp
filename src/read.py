import struct
from .consts.pointers import FUNC, PNTR, LUAV
from .consts.functions import FUNCTION_NAMES
from .globals import *
from . import prints

ORD_a = ord('a')
ORD_z = ord('z')
ORD_A = ord('A')
ORD_Z = ord('Z')
ORD_0 = ord('0')
ORD_9 = ord('9')
ORD_UNDERSCORE = ord('_')


def read_u8(buffer: bytes, index: int) -> int:
    return int.from_bytes(buffer[index:index+1], byteorder="little", signed=False)


def read_u16(buffer: bytes, index: int) -> int:
    return int.from_bytes(buffer[index:index+2], byteorder="little", signed=False)


def read_u32(buffer: bytes, index: int) -> int:
    return int.from_bytes(buffer[index:index+4], byteorder="little", signed=False)


def read_s8(buffer: bytes, index: int) -> int:
    return int.from_bytes(buffer[index:index+1], byteorder="little", signed=True)


def read_s16(buffer: bytes, index: int) -> int:
    return int.from_bytes(buffer[index:index+2], byteorder="little", signed=True)


def read_s32(buffer: bytes, index: int) -> int:
    return int.from_bytes(buffer[index:index+4], byteorder="little", signed=True)


def read_f32(buffer: bytes, index: int) -> float:
    return float(struct.unpack("<f", buffer[index:index+4])[0])


def read_name(buffer: bytes, index: int) -> tuple[str, int]:
    global g_options
    length = read_u8(buffer, index)
    if not g_options.get(OPT_ADVANCED_MODE):
        return buffer[index + 1:index + 1 + length].decode("utf-8"), index + 1 + length

    # [Advanced mode] ignore length, read name until invalid char
    def valid_char(c):
        return (c >= ORD_a and c <= ORD_z) or (c >= ORD_A and c <= ORD_Z) or (c >= ORD_0 and c <= ORD_9) or (c == ORD_UNDERSCORE)
    index += 1
    index_start = index
    while index < len(buffer) and valid_char(buffer[index]):
        index += 1
    return buffer[index_start:index].decode("utf-8"), index


def read_buffer(buffer: bytes, index: int, read_length_func, read_data_func) -> tuple[list, int]:
    length, index = read_length_func(buffer, index)
    output = list()
    for _ in range(length):
        value, index = read_data_func(buffer, index)
        output.append(value)
    return output, index


def read_pointer(buffer: bytes, index: int, ignore_pointer_offset: bool) -> tuple[str|int, int]:
    value = read_u32(buffer, index)
    index += 4
    if value == FUNC:
        value = read_u32(buffer, index)
        if value < len(FUNCTION_NAMES):
            value = FUNCTION_NAMES[value]
        else:
            prints.warning("%08X    [Warning!] Unknown function index: %d" % (index, value), nowarn=True)
            value = "unknown_func_%d" % (value)
        index += 4
    elif value == PNTR:
        index_ptr = index - 4
        value, index = read_name(buffer, index)
        offset = read_u32(buffer, index)
        if not ignore_pointer_offset:
            value += " + %d" % (offset)
        elif offset != 0:
            prints.warning("%08X    [Warning!] Non-zero offset on pointer %s: %d" % (index_ptr, value, offset), nowarn=True)
        index += 4
    elif value == LUAV:
        value, index = read_name(buffer, index)
    return value, index
