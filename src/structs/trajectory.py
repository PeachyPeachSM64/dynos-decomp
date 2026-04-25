from dataclasses import dataclass, field
from ..read import *


@dataclass
class Trajectory:
    buffer: list = field(default_factory=lambda: [])

    @staticmethod
    def read(buffer: bytes, index: int):
        trajectory = Trajectory()
        length = read_u32(buffer, index)
        index += 4
        for _ in range(length):
            cmd = read_s16(buffer, index)
            trajectory.buffer.append(cmd)
            index += 2
        return trajectory, index
