import struct


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
