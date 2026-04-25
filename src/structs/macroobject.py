from dataclasses import dataclass, field
from ..read import *


@dataclass
class MacroObject:
    buffer: list = field(default_factory=lambda: [])

    @staticmethod
    def read(buffer: bytes, index: int):
        macroobject = MacroObject()
        length = read_u32(buffer, index)
        index += 4
        for _ in range(length):
            cmd = read_s16(buffer, index)
            macroobject.buffer.append(cmd)
            index += 2
        return macroobject, index
