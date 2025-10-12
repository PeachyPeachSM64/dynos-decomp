from dataclasses import dataclass, field
from ..consts.functions import FUNCTION_NAMES
from ..read import *


@dataclass
class BehaviorScript:
    buffer: list = field(default_factory=lambda: [])

    @staticmethod
    def read(buffer: bytes, index: int):
        behavior = BehaviorScript()
        index += 3 # version stuff, not needed
        length = read_u32(buffer, index)
        index += 4
        for _ in range(length):
            value, index = read_pointer(buffer, index, True)
            behavior.buffer.append(value)
        return behavior, index

