from dataclasses import dataclass, field
from .read import *


F32VTX_SENTINEL_0 = 0x3346
F32VTX_SENTINEL_1 = 0x5632
F32VTX_SENTINEL_2 = 0x5854


@dataclass
class Vertex:
    x: float = 0
    y: float = 0
    z: float = 0
    f: int = 0
    u: int = 0
    v: int = 0
    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 0

    @staticmethod
    def read(buffer: bytes, index: int, f32_vtx: bool):
        vtx = Vertex()
        if f32_vtx:
            vtx.x = read_f32(buffer, index + 0)
            vtx.y = read_f32(buffer, index + 4)
            vtx.z = read_f32(buffer, index + 8)
            vtx.f = read_s16(buffer, index + 12)
            vtx.u = read_s16(buffer, index + 14)
            vtx.v = read_s16(buffer, index + 16)
            vtx.r = read_u8(buffer, index + 18)
            vtx.g = read_u8(buffer, index + 19)
            vtx.b = read_u8(buffer, index + 20)
            vtx.a = read_u8(buffer, index + 21)
            index += 22
        else:
            vtx.x = read_s16(buffer, index + 0)
            vtx.y = read_s16(buffer, index + 2)
            vtx.z = read_s16(buffer, index + 4)
            vtx.f = read_s16(buffer, index + 6)
            vtx.u = read_s16(buffer, index + 8)
            vtx.v = read_s16(buffer, index + 10)
            vtx.r = read_u8(buffer, index + 12)
            vtx.g = read_u8(buffer, index + 13)
            vtx.b = read_u8(buffer, index + 14)
            vtx.a = read_u8(buffer, index + 15)
            index += 16
        return vtx, index


@dataclass
class VertexArray:
    buffer: list = field(default_factory=lambda: [])

    @staticmethod
    def read(buffer: bytes, index: int):
        vtxarr = VertexArray()
        length = read_u32(buffer, index)
        index += 4
        f32_vtx = False
        for _ in range(length):
            vtx, index = Vertex.read(buffer, index, f32_vtx)
            if not f32_vtx and vtx.x == F32VTX_SENTINEL_0 and vtx.y == F32VTX_SENTINEL_1 and vtx.z == F32VTX_SENTINEL_2:
                f32_vtx = True
            else:
                vtxarr.buffer.append(vtx)
        return vtxarr, index
