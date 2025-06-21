from dataclasses import dataclass
from .read import *


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
