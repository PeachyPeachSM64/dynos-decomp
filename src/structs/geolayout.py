from dataclasses import dataclass, field
from ..consts.consts import FUNC, PNTR, LUAV
from ..consts.functions import FUNCTION_NAMES
from ..read import *


@dataclass
class GeoLayout:
    buffer: list = field(default_factory=lambda: [])

    @staticmethod
    def read(buffer: bytes, index: int):
        geolayout = GeoLayout()
        length = read_u32(buffer, index)
        index += 4
        for _ in range(length):
            value = read_u32(buffer, index)
            index += 4
            if value == FUNC:
                value = read_u32(buffer, index)
                value = FUNCTION_NAMES[value]
                index += 4
            elif value == PNTR:
                value, index = read_name(buffer, index)
                # value += " + %d" % (read_u32(buffer, index))
                index += 4
            elif value == LUAV:
                value, index = read_name(buffer, index)
            geolayout.buffer.append(value)
        return geolayout, index

