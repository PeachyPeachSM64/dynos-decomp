from dataclasses import dataclass, field
from ..read import *


@dataclass
class LevelScript:
    buffer: list = field(default_factory=lambda: [])

    @staticmethod
    def read(buffer: bytes, index: int):
        level = LevelScript()
        length = read_u32(buffer, index)
        index += 4
        for _ in range(length):
            value, index = read_pointer(buffer, index, True)
            level.buffer.append(value)
        return level, index
