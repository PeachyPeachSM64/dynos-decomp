from dataclasses import dataclass, field
from . import prints
from .read import *
from .consts.types import DATA_TYPE_NONE
from .structs.lights import Light, Ambient, Lights1
from .structs.texture import Texture, TextureList
from .structs.vertex import VertexArray
from .structs.displaylist import DisplayList
from .structs.geolayout import GeoLayout
from .structs.animation import Animation
from .structs.behavior import BehaviorScript


@dataclass
class GfxData:
    lights: dict[str, Light] = field(default_factory=lambda: {})
    ambients: dict[str, Ambient] = field(default_factory=lambda: {})
    lights1: dict[str, Lights1] = field(default_factory=lambda: {})
    textures: dict[str, Texture] = field(default_factory=lambda: {})
    texture_lists: dict[str, TextureList] = field(default_factory=lambda: {}) # actually backgrounds
    vertices: dict[str, VertexArray] = field(default_factory=lambda: {})
    displaylists: dict[str, DisplayList] = field(default_factory=lambda: {})
    geolayouts: dict[str, GeoLayout] = field(default_factory=lambda: {})
    animations: dict[str, Animation] = field(default_factory=lambda: {})
    animation_table: list[str] = field(default_factory=lambda: [])
    behaviors: dict[str, BehaviorScript] = field(default_factory=lambda: {})
    priority: int = 0

    @staticmethod
    def writer():
        def writer(func):
            setattr(GfxData, func.__name__, func)
            return func
        return writer

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

    def read_texture_list(self, buffer: bytes, index: int):
        name, index = read_name(buffer, index)
        data, index = TextureList.read(buffer, index)
        self.texture_lists[name] = data
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

    def read_gfxdyncmd(self, buffer: bytes, index: int):
        name, index = read_name(buffer, index)
        return index + 5, name

    def read_behavior(self, buffer: bytes, index: int):
        name, index = read_name(buffer, index)
        data, index = BehaviorScript.read(buffer, index)
        self.behaviors[name] = data
        return index, name

    def read_priority(self, buffer: bytes, index: int):
        self.priority = read_u8(buffer, index)
        return index + 1, "priority: %02X" % (self.priority)

    @staticmethod
    def read(buffer: bytes, data_types: dict):
        from .datatypes import DATA_TYPES
        length = len(buffer)
        index = 0
        gfx = GfxData()
        while index < length:
            data_type = read_u8(buffer, index)
            index_data = index
            index += 1

            # End of file
            if data_type == DATA_TYPE_NONE:
                break

            # Unknown type
            if data_type not in DATA_TYPES:
                prints.warning("\n%08X    [!] Unknown data type: %d" % (index_data, data_type))
                break

            data_type_name = DATA_TYPES[data_type]["name"]
            data_type_read = DATA_TYPES[data_type]["read"]

            # Check allowed
            data_type_used = data_types.get(data_type)
            if data_type_used is None:
                prints.warning("\n%08X    [!] Data type not allowed: %s" % (index_data, data_type_name))
                break

            prints.info("%08X    %-16s " % (index_data, data_type_name), end="")
            index, name = data_type_read(gfx, buffer, index)
            prints.info(name)

            # Check unused
            if not data_type_used:
                prints.warning("\n%08X    [!] Unused data type: %s" % (index_data, data_type_name))

        return gfx
