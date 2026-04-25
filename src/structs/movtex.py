from dataclasses import dataclass, field
from ..read import *


@dataclass
class Movtex:
    buffer: list = field(default_factory=lambda: [])

    @staticmethod
    def read(buffer: bytes, index: int):
        movtex = Movtex()
        length = read_u32(buffer, index)
        index += 4
        for _ in range(length):
            cmd = read_s16(buffer, index)
            movtex.buffer.append(cmd)
            index += 2
        return movtex, index


@dataclass
class MovtexQC:
    buffer: dict[int, str] = field(default_factory=lambda: {})

    @staticmethod
    def read(buffer: bytes, index: int):
        movtexqc = MovtexQC()
        length = read_u32(buffer, index)
        index += 4
        for _ in range(length):
            id = read_s16(buffer, index)
            index_ptr = index + 2
            value, index = read_pointer(buffer, index_ptr, True)
            if isinstance(value, str) or value == 0:
                movtexqc.buffer[id] = str(value)
            else:
                prints.warning("%08X    [Warning!] Invalid Movtex reference (expected name): %08X" % (index_ptr, value), nowarn=True)
        return movtexqc, index
