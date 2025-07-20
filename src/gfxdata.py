from dataclasses import dataclass, field
from . import prints
from .read import *
from .lights import Light, Ambient, Lights1
from .texture import Texture
from .vertex import VertexArray
from .displaylist import DisplayList
from .geolayout import GeoLayout
from .animation import Animation


@dataclass
class GfxData:
    lights: dict[str, Light] = field(default_factory=lambda: {})
    ambients: dict[str, Ambient] = field(default_factory=lambda: {})
    lights1: dict[str, Lights1] = field(default_factory=lambda: {})
    textures: dict[str, Texture] = field(default_factory=lambda: {})
    vertices: dict[str, VertexArray] = field(default_factory=lambda: {})
    displaylists: dict[str, DisplayList] = field(default_factory=lambda: {})
    geolayouts: dict[str, GeoLayout] = field(default_factory=lambda: {})
    animations: dict[str, Animation] = field(default_factory=lambda: {})
    animation_table: list[str] = field(default_factory=lambda: [])
    priority: int = 0

    def read_light(self, buffer: bytes, index: int):
        name, index = read_name(buffer, index)
        data, index = Light.read(buffer, index)
        self.lights[name] = data
        return index, name

    def read_ambient(self, buffer: bytes, index: int):
        name, index = read_name(buffer, index)
        data, index = Ambient.read(buffer, index)
        self.ambients[name] = data
        return index, name

    def read_lights1(self, buffer: bytes, index: int):
        name, index = read_name(buffer, index)
        data, index = Lights1.read(buffer, index)
        self.lights1[name] = data
        return index, name

    def read_texture(self, buffer: bytes, index: int):
        name, index = read_name(buffer, index)
        data, index = Texture.read(buffer, index, False)
        self.textures[name] = data
        return index, name

    def read_texture_raw(self, buffer: bytes, index: int):
        name, index = read_name(buffer, index)
        data, index = Texture.read(buffer, index, True)
        self.textures[name] = data
        return index, name

    def read_vertex(self, buffer: bytes, index: int):
        name, index = read_name(buffer, index)
        data, index = VertexArray.read(buffer, index)
        self.vertices[name] = data
        return index, name

    def read_display_list(self, buffer: bytes, index: int):
        name, index = read_name(buffer, index)
        data, index = DisplayList.read(buffer, index)
        self.displaylists[name] = data
        return index, name

    def read_geo_layout(self, buffer: bytes, index: int):
        name, index = read_name(buffer, index)
        data, index = GeoLayout.read(buffer, index)
        self.geolayouts[name] = data
        return index, name

    def read_animation(self, buffer: bytes, index: int):
        name, index = read_name(buffer, index)
        data, index = Animation.read(buffer, index)
        self.animations[name] = data
        return index, name

    def read_animation_table(self, buffer: bytes, index: int):
        name, index = read_name(buffer, index)
        self.animation_table.append(name)
        return index, name

    def read_priority(self, buffer: bytes, index: int):
        self.priority = read_u8(buffer, index)
        return index + 1, "priority: %02X" % (self.priority)

    @staticmethod
    def read(buffer: bytes):
        from .datatypes import DATA_TYPES
        length = len(buffer)
        index = 0
        gfx = GfxData()
        while index < length:
            data_type = read_u8(buffer, index)
            index += 1
            if data_type in DATA_TYPES:
                prints.info("%08X    %-16s " % (index - 1, DATA_TYPES[data_type]["name"]), end="")
                index, name = DATA_TYPES[data_type]["read"](gfx, buffer, index)
                prints.info(name)
            else:
                prints.warning("\n%08X    [!] Unknown data type: %d" % (index - 1, data_type))
                break
        return gfx
