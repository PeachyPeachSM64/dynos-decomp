from dataclasses import dataclass, field
from ..consts.pointers import PNTR
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
            w1 = read_u32(buffer, index + 4)
            index += 8
            if w1 == PNTR:
                w1, index = read_name(buffer, index)
                w1 += " + %d" % (read_u32(buffer, index))
                index += 4
            displaylist.buffer.append(w0)
            displaylist.buffer.append(w1)
        return displaylist, index
