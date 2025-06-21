from dataclasses import dataclass
from .consts import TEXR
from .read import *


@dataclass
class Texture:
    png: bytes | None = None
    ref: str | None = None

    @staticmethod
    def read(buffer: bytes, index: int):
        texture = Texture()
        length_or_texr = read_u32(buffer, index)
        if length_or_texr == TEXR:
            texture.ref, index = read_name(buffer, index + 4)
            return texture, index
        texture.png = bytes(buffer[index + 4:index + 4 + length_or_texr])
        return texture, index + 4 + length_or_texr
