from .gfxdata import GfxData
from .consts.types import *


def not_implemented(*_):
    raise Exception("Not implemented")


DATA_TYPES = {

DATA_TYPE_NONE: {
    "name": "NONE",
    "read": not_implemented,
},
DATA_TYPE_LIGHT: {
    "name": "LIGHT",
    "read": GfxData.read_lights1,
},
DATA_TYPE_TEXTURE: {
    "name": "TEXTURE",
    "read": GfxData.read_texture,
},
DATA_TYPE_VERTEX: {
    "name": "VERTEX",
    "read": GfxData.read_vertex,
},
DATA_TYPE_DISPLAY_LIST: {
    "name": "DISPLAY_LIST",
    "read": GfxData.read_display_list,
},
DATA_TYPE_GEO_LAYOUT: {
    "name": "GEO_LAYOUT",
    "read": GfxData.read_geo_layout,
},
DATA_TYPE_ANIMATION_VALUE: {
    "name": "ANIMATION_VALUE",
    "read": not_implemented,
},
DATA_TYPE_ANIMATION_INDEX: {
    "name": "ANIMATION_INDEX",
    "read": not_implemented,
},
DATA_TYPE_ANIMATION: {
    "name": "ANIMATION",
    "read": GfxData.read_animation,
},
DATA_TYPE_ANIMATION_TABLE: {
    "name": "ANIMATION_TABLE",
    "read": GfxData.read_animation_table,
},
DATA_TYPE_GFXDYNCMD: {
    "name": "GFXDYNCMD",
    "read": GfxData.read_gfxdyncmd,
},
DATA_TYPE_COLLISION: {
    "name": "COLLISION",
    "read": GfxData.read_collision,
},
DATA_TYPE_LEVEL_SCRIPT: {
    "name": "LEVEL_SCRIPT",
    "read": not_implemented,
},
DATA_TYPE_MACRO_OBJECT: {
    "name": "MACRO_OBJECT",
    "read": not_implemented,
},
DATA_TYPE_TRAJECTORY: {
    "name": "TRAJECTORY",
    "read": not_implemented,
},
DATA_TYPE_MOVTEX: {
    "name": "MOVTEX",
    "read": not_implemented,
},
DATA_TYPE_MOVTEXQC: {
    "name": "MOVTEXQC",
    "read": not_implemented,
},
DATA_TYPE_ROOMS: {
    "name": "ROOMS",
    "read": not_implemented,
},
DATA_TYPE_LIGHT_T: {
    "name": "LIGHT_T",
    "read": GfxData.read_light,
},
DATA_TYPE_AMBIENT_T: {
    "name": "AMBIENT_T",
    "read": GfxData.read_ambient,
},
DATA_TYPE_TEXTURE_LIST: {
    "name": "TEXTURE_LIST",
    "read": GfxData.read_texture_list,
},
DATA_TYPE_TEXTURE_RAW: {
    "name": "TEXTURE_RAW",
    "read": GfxData.read_texture_raw,
},
DATA_TYPE_BEHAVIOR_SCRIPT: {
    "name": "BEHAVIOR_SCRIPT",
    "read": GfxData.read_behavior,
},
DATA_TYPE_UNUSED: {
    "name": "UNUSED",
    "read": not_implemented,
},
DATA_TYPE_LIGHT_0: {
    "name": "LIGHT_0",
    "read": GfxData.read_lights1, # Note: internally, Lights0 struct is the same as Lights1
},
DATA_TYPE_PRIORITY: {
    "name": "PRIORITY",
    "read": GfxData.read_priority,
},

}
