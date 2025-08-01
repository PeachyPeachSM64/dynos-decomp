from dataclasses import dataclass
from ..read import *


@dataclass
class Light:
    cr: int = 0
    cg: int = 0
    cb: int = 0
    c2r: int = 0
    c2g: int = 0
    c2b: int = 0
    dx: int = 0
    dy: int = 0
    dz: int = 0

    @staticmethod
    def read(buffer: bytes, index: int):
        light = Light()
        light.cr = read_u8(buffer, index + 0)
        light.cg = read_u8(buffer, index + 1)
        light.cb = read_u8(buffer, index + 2)
        light.c2r = read_u8(buffer, index + 4)
        light.c2g = read_u8(buffer, index + 5)
        light.c2b = read_u8(buffer, index + 6)
        light.dx = read_s8(buffer, index + 8)
        light.dy = read_s8(buffer, index + 9)
        light.dz = read_s8(buffer, index + 10)
        return light, index + 12


@dataclass
class Ambient:
    cr: int = 0
    cg: int = 0
    cb: int = 0
    c2r: int = 0
    c2g: int = 0
    c2b: int = 0

    @staticmethod
    def read(buffer: bytes, index: int):
        ambient = Ambient()
        ambient.cr = read_u8(buffer, index + 0)
        ambient.cg = read_u8(buffer, index + 1)
        ambient.cb = read_u8(buffer, index + 2)
        ambient.c2r = read_u8(buffer, index + 4)
        ambient.c2g = read_u8(buffer, index + 5)
        ambient.c2b = read_u8(buffer, index + 6)
        return ambient, index + 8


@dataclass
class Lights1:
    ar: int = 0
    ag: int = 0
    ab: int = 0
    r1: int = 0
    g1: int = 0
    b1: int = 0
    x1: int = 0
    y1: int = 0
    z1: int = 0

    @staticmethod
    def read(buffer: bytes, index: int):
        lights1 = Lights1()
        lights1.ar = read_u8(buffer, index + 0)
        lights1.ag = read_u8(buffer, index + 1)
        lights1.ab = read_u8(buffer, index + 2)
        lights1.r1 = read_u8(buffer, index + 8)
        lights1.g1 = read_u8(buffer, index + 9)
        lights1.b1 = read_u8(buffer, index + 10)
        lights1.x1 = read_u8(buffer, index + 16)
        lights1.y1 = read_u8(buffer, index + 17)
        lights1.z1 = read_u8(buffer, index + 18)
        return lights1, index + 24
