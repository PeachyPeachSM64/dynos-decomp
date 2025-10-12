from dataclasses import dataclass, field
from ..read import *


@dataclass
class DisplayList:
    buffer: list = field(default_factory=lambda: [])

    @staticmethod
    def read(buffer: bytes, index: int):
        displaylist = DisplayList()
        length = read_u32(buffer, index)
        index += 4
        for _ in range(length):
            w0 = read_u32(buffer, index)
            w1, index = read_pointer(buffer, index + 4, False)
            displaylist.buffer.append(w0)
            displaylist.buffer.append(w1)
        return displaylist, index
