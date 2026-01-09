from dataclasses import dataclass, field
from ..read import *


@dataclass
class Collision:
    buffer: list = field(default_factory=lambda: [])

    @staticmethod
    def read(buffer: bytes, index: int):
        collision = Collision()
        length = read_u32(buffer, index)
        index += 4
        for _ in range(length):
            col = read_u16(buffer, index)
            collision.buffer.append(col)
            index += 2
        return collision, index
