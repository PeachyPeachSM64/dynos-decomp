import png
from dataclasses import dataclass, field
from .. import prints
from ..consts.pointers import TEXR
from ..read import *

PNG_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])

# Image formats
G_IM_FMT_RGBA = 0
G_IM_FMT_IA = 3
G_IM_FMT_I = 4

# Image sizes
G_IM_SIZ_4b = 0
G_IM_SIZ_8b = 1
G_IM_SIZ_16b = 2
G_IM_SIZ_32b = 3

# Image types
G_IM_RGBA16 = (G_IM_FMT_RGBA << 4 | G_IM_SIZ_16b)
G_IM_RGBA32 = (G_IM_FMT_RGBA << 4 | G_IM_SIZ_32b)
G_IM_IA4 = (G_IM_FMT_IA << 4 | G_IM_SIZ_4b) 
G_IM_IA8 = (G_IM_FMT_IA << 4 | G_IM_SIZ_8b) 
G_IM_IA16 = (G_IM_FMT_IA << 4 | G_IM_SIZ_16b)
G_IM_I4 = (G_IM_FMT_I << 4 | G_IM_SIZ_4b) 
G_IM_I8 = (G_IM_FMT_I << 4 | G_IM_SIZ_8b) 


SCALE_5_8 = lambda x: (x * 0xFF) // 0x1F
SCALE_8_5 = lambda x: ((x + 4) * 0x1F) // 0xFF
SCALE_4_8 = lambda x: x * 0x11
SCALE_8_4 = lambda x: x // 0x11
SCALE_3_8 = lambda x: x * 0x24
SCALE_8_3 = lambda x: x // 0x24


@dataclass
class RawTextureData:
    fmt: int = 0
    siz: int = 0
    width: int = 0
    height: int = 0
    data: bytes = field(default_factory=lambda: bytes())

    def rgba16_to_rgba32(self) -> bytes:
        buf = bytearray()
        for i in range(0, len(self.data), 2):
            c = (self.data[i + 0] << 8) | self.data[i + 1]
            r = (c >> 11) & 0x1F
            g = (c >>  6) & 0x1F
            b = (c >>  1) & 0x1F
            a = (c >>  0) & 0x01
            buf.append(SCALE_5_8(r))
            buf.append(SCALE_5_8(g))
            buf.append(SCALE_5_8(b))
            buf.append(0xFF * (a))
        return bytes(buf)

    def ia4_to_rgba32(self) -> bytes:
        buf = bytearray()
        for i in range(0, len(self.data), 1):
            h0 = (self.data[i] >> 4) & 0xF
            buf.append(SCALE_3_8(h0 >> 1))
            buf.append(SCALE_3_8(h0 >> 1))
            buf.append(SCALE_3_8(h0 >> 1))
            buf.append(0xFF * (h0 & 1))
            h1 = (self.data[i] >> 0) & 0xF
            buf.append(SCALE_3_8(h1 >> 1))
            buf.append(SCALE_3_8(h1 >> 1))
            buf.append(SCALE_3_8(h1 >> 1))
            buf.append(0xFF * (h1 & 1))
        return bytes(buf)

    def ia8_to_rgba32(self) -> bytes:
        buf = bytearray()
        for i in range(0, len(self.data), 1):
            c = (self.data[i] >> 4) & 0xF
            a = (self.data[i] >> 0) & 0xF
            buf.append(SCALE_4_8(c))
            buf.append(SCALE_4_8(c))
            buf.append(SCALE_4_8(c))
            buf.append(SCALE_4_8(a))
        return bytes(buf)

    def ia16_to_rgba32(self) -> bytes:
        buf = bytearray()
        for i in range(0, len(self.data), 2):
            c = self.data[i + 0]
            a = self.data[i + 1]
            buf.append(c)
            buf.append(c)
            buf.append(c)
            buf.append(a)
        return bytes(buf)

    def i4_to_rgba32(self) -> bytes:
        buf = bytearray()
        for i in range(0, len(self.data), 1):
            h0 = (self.data[i] >> 4) & 0xF
            buf.append(SCALE_4_8(h0))
            buf.append(SCALE_4_8(h0))
            buf.append(SCALE_4_8(h0))
            buf.append(255)
            h1 = (self.data[i] >> 0) & 0xF
            buf.append(SCALE_4_8(h1))
            buf.append(SCALE_4_8(h1))
            buf.append(SCALE_4_8(h1))
            buf.append(255)
        return bytes(buf)

    def i8_to_rgba32(self) -> bytes:
        buf = bytearray()
        for i in range(0, len(self.data), 1):
            buf.append(self.data[i])
            buf.append(self.data[i])
            buf.append(self.data[i])
            buf.append(255)
        return bytes(buf)

    def convert_to_rgba32(self) -> bytes|None:
        img_type = (self.fmt << 4 | self.siz)
        if img_type == G_IM_RGBA16: return self.rgba16_to_rgba32() 
        if img_type == G_IM_RGBA32: return bytes(self.data)
        if img_type == G_IM_IA4: return self.ia4_to_rgba32()
        if img_type == G_IM_IA8: return self.ia8_to_rgba32()
        if img_type == G_IM_IA16: return self.ia16_to_rgba32()
        if img_type == G_IM_I4: return self.i4_to_rgba32()
        if img_type == G_IM_I8: return self.i8_to_rgba32()
        prints.warning("Unknown image type: fmt: %d, siz: %d" % (self.fmt, self.siz))
        return None

    def write(self, filepath: str) -> bool:
        rgba32 = self.convert_to_rgba32()
        if rgba32:
            img = []
            for y in range(self.height):
                row = ()
                for x in range(self.width):
                    r = rgba32[((self.width * y) + x) * 4 + 0]
                    g = rgba32[((self.width * y) + x) * 4 + 1]
                    b = rgba32[((self.width * y) + x) * 4 + 2]
                    a = rgba32[((self.width * y) + x) * 4 + 3]
                    row = row + (r, g, b, a)
                img.append(row)
            with open(filepath, "wb") as f:
                w = png.Writer(self.width, self.height, greyscale=False, alpha='RGBA')
                w.write(f, img)
            return True
        return False


@dataclass
class Texture:
    png: bytes|None = None
    raw: RawTextureData|None = None
    ref: str|None = None

    @staticmethod
    def read(buffer: bytes, index: int, raw: bool):
        texture = Texture()
        if raw:
            raw_length = read_u32(buffer, index + 16)
            texture.raw = RawTextureData(
                fmt=read_u32(buffer, index),
                siz=read_u32(buffer, index + 4),
                width=read_u32(buffer, index + 8),
                height=read_u32(buffer, index + 12),
                data=bytes(buffer[index + 20:index + 20 + raw_length])
            )
            return texture, index + 20 + raw_length
        length_or_texr = read_u32(buffer, index)
        if length_or_texr == TEXR:
            texture.ref, index = read_name(buffer, index + 4)
            return texture, index
        png_sig = bytes(buffer[index + 4: index + 4 + len(PNG_MAGIC)])
        if png_sig == PNG_MAGIC:
            texture.png = bytes(buffer[index + 4:index + 4 + length_or_texr])
        return texture, index + 4 + length_or_texr

    def write(self, filepath: str) -> bool:
        if self.raw is not None:
            return self.raw.write(filepath)
        if self.png is not None:
            with open(filepath, "wb") as f:
                f.write(self.png)
            return True
        return False


@dataclass
class TextureList:
    textures: list[str] = field(default_factory=lambda: [])

    @staticmethod
    def read(buffer: bytes, index: int):
        texlist = TextureList()
        length = read_u32(buffer, index)
        index += 4
        for _ in range(length):
            index_ptr = index
            value, index = read_pointer(buffer, index, True)
            if isinstance(value, str):
                texlist.textures.append(value)
            else:
                prints.warning("\n%08X    [!] Invalid texture (expected name): %08X" % (index_ptr, value))
                texlist.textures.append("")
        return texlist, index
