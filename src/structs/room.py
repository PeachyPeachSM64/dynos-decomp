from dataclasses import dataclass, field
from ..read import *


@dataclass
class Room:
    buffer: list = field(default_factory=lambda: [])

    @staticmethod
    def read(buffer: bytes, index: int):
        room = Room()
        length = read_u32(buffer, index)
        index += 4
        for _ in range(length):
            id = read_u8(buffer, index)
            room.buffer.append(id)
            index += 2
        return room, index
