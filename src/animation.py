from dataclasses import dataclass, field
from .read import *


@dataclass
class Animation:
    flags: int = 0
    anim_y_trans_div: int = 0
    start_frame: int = 0
    loop_start: int = 0
    loop_end: int = 0
    bone_count: int = 0
    length: int = 0
    values: list = field(default_factory=lambda: [])
    index: list = field(default_factory=lambda: [])

    @staticmethod
    def read(buffer: bytes, index: int):
        animation = Animation()
        animation.flags = read_s16(buffer, index + 0)
        animation.anim_y_trans_div = read_s16(buffer, index + 2)
        animation.start_frame = read_s16(buffer, index + 4)
        animation.loop_start = read_s16(buffer, index + 6)
        animation.loop_end = read_s16(buffer, index + 8)
        animation.bone_count = read_s16(buffer, index + 10)
        animation.length = read_u32(buffer, index + 12)
        index += 16
        animation.values, index = read_buffer(buffer, index,
            lambda buffer, index: (read_s32(buffer, index), index + 4),
            lambda buffer, index: (read_s16(buffer, index), index + 2)
        )
        animation.index, index = read_buffer(buffer, index,
            lambda buffer, index: (read_s32(buffer, index), index + 4),
            lambda buffer, index: (read_u16(buffer, index), index + 2)
        )
        return animation, index
