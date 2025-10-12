from dataclasses import dataclass, field
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
            value, index = read_pointer(buffer, index, True)
            geolayout.buffer.append(value)
        return geolayout, index

