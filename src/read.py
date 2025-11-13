import struct
from .consts.pointers import FUNC, PNTR, LUAV
from .consts.functions import FUNCTION_NAMES
from . import prints


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
    length = read_u8(buffer, index)
    return buffer[index + 1:index + 1 + length].decode("utf-8"), index + 1 + length


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
        value = FUNCTION_NAMES[value]
        index += 4
    elif value == PNTR:
        index_ptr = index - 4
        value, index = read_name(buffer, index)
        offset = read_u32(buffer, index)
        if not ignore_pointer_offset:
            value += " + %d" % (offset)
        elif offset != 0:
            prints.warning("\n%08X    [!] Non-zero offset on pointer %s: %d" % (index_ptr, value, offset))
        index += 4
    elif value == LUAV:
        value, index = read_name(buffer, index)
    return value, index
