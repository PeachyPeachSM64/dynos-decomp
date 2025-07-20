from .gfxdata import GfxData


def not_implemented(*_):
    raise Exception("Not implemented")


DATA_TYPES = {

0: {
    "name": "NONE",
    "read": not_implemented,
},
1: {
    "name": "LIGHT",
    "read": GfxData.read_lights1,
},
2: {
    "name": "TEXTURE",
    "read": GfxData.read_texture,
},
3: {
    "name": "VERTEX",
    "read": GfxData.read_vertex,
},
4: {
    "name": "DISPLAY_LIST",
    "read": GfxData.read_display_list,
},
5: {
    "name": "GEO_LAYOUT",
    "read": GfxData.read_geo_layout,
},
6: {
    "name": "ANIMATION_VALUE",
    "read": not_implemented,
},
7: {
    "name": "ANIMATION_INDEX",
    "read": not_implemented,
},
8: {
    "name": "ANIMATION",
    "read": GfxData.read_animation,
},
9: {
    "name": "ANIMATION_TABLE",
    "read": GfxData.read_animation_table,
},
10: {
    "name": "GFXDYNCMD",
    "read": not_implemented,
},
11: {
    "name": "COLLISION",
    "read": not_implemented,
},
12: {
    "name": "LEVEL_SCRIPT",
    "read": not_implemented,
},
13: {
    "name": "MACRO_OBJECT",
    "read": not_implemented,
},
14: {
    "name": "TRAJECTORY",
    "read": not_implemented,
},
15: {
    "name": "MOVTEX",
    "read": not_implemented,
},
16: {
    "name": "MOVTEXQC",
    "read": not_implemented,
},
17: {
    "name": "ROOMS",
    "read": not_implemented,
},
18: {
    "name": "LIGHT_T",
    "read": GfxData.read_light,
},
19: {
    "name": "AMBIENT_T",
    "read": GfxData.read_ambient,
},
20: {
    "name": "TEXTURE_LIST",
    "read": not_implemented,
},
21: {
    "name": "TEXTURE_RAW",
    "read": GfxData.read_texture_raw,
},
22: {
    "name": "BEHAVIOR_SCRIPT",
    "read": not_implemented,
},
23: {
    "name": "UNUSED",
    "read": not_implemented,
},
24: {
    "name": "LIGHT_0",
    "read": not_implemented,
},
0xFF: {
    "name": "PRIORITY",
    "read": GfxData.read_priority,
},

}
