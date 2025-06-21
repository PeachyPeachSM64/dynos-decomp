import os
from .gfxdata import GfxData


GEO_CONSTANTS = {
    "layer": {
        "0": "LAYER_FORCE",
        "1": "LAYER_OPAQUE",
        "2": "LAYER_OPAQUE_DECAL",
        "3": "LAYER_OPAQUE_INTER",
        "4": "LAYER_ALPHA",
        "5": "LAYER_TRANSPARENT",
        "6": "LAYER_TRANSPARENT_DECAL",
        "7": "LAYER_TRANSPARENT_INTER",
    },
    "shadowType": {
        "0": "SHADOW_CIRCLE_9_VERTS",
        "1": "SHADOW_CIRCLE_4_VERTS",
        "2": "SHADOW_CIRCLE_4_VERTS_FLAT_UNUSED",
        "3": "SHADOW_SPIKE_EXT",
        "10": "SHADOW_SQUARE_PERMANENT",
        "11": "SHADOW_SQUARE_SCALABLE",
        "12": "SHADOW_SQUARE_TOGGLABLE",
        "50": "SHADOW_RECTANGLE_HARDCODED_OFFSET",
        "99": "SHADOW_CIRCLE_PLAYER",
    },
    "background": {
        "0": "BACKGROUND_OCEAN_SKY",
        "1": "BACKGROUND_FLAMING_SKY",
        "2": "BACKGROUND_UNDERWATER_CITY",
        "3": "BACKGROUND_BELOW_CLOUDS",
        "4": "BACKGROUND_SNOW_MOUNTAINS",
        "5": "BACKGROUND_DESERT",
        "6": "BACKGROUND_HAUNTED",
        "7": "BACKGROUND_GREEN_SKY",
        "8": "BACKGROUND_ABOVE_CLOUDS",
        "9": "BACKGROUND_PURPLE_SKY",
        "10": "BACKGROUND_CUSTOM",
    },
    "cameraMode": {
        "0": "CAMERA_MODE_NONE",
        "1": "CAMERA_MODE_RADIAL",
        "2": "CAMERA_MODE_OUTWARD_RADIAL",
        "3": "CAMERA_MODE_BEHIND_MARIO",
        "4": "CAMERA_MODE_CLOSE",
        "6": "CAMERA_MODE_C_UP",
        "8": "CAMERA_MODE_WATER_SURFACE",
        "9": "CAMERA_MODE_SLIDE_HOOT",
        "10": "CAMERA_MODE_INSIDE_CANNON",
        "11": "CAMERA_MODE_BOSS_FIGHT",
        "12": "CAMERA_MODE_PARALLEL_TRACKING",
        "13": "CAMERA_MODE_FIXED",
        "14": "CAMERA_MODE_8_DIRECTIONS",
        "16": "CAMERA_MODE_FREE_ROAM",
        "17": "CAMERA_MODE_SPIRAL_STAIRS",
        "18": "CAMERA_MODE_NEWCAM",
        "19": "CAMERA_MODE_ROM_HACK",
    },
}


def CMD_BBBB(a, b, c, d):
    return [
        {"value": a, "shift": 0, "width": 8},
        {"value": b, "shift": 8, "width": 8},
        {"value": c, "shift": 16, "width": 8},
        {"value": d, "shift": 24, "width": 8},
    ]


def CMD_BBH(a, b, c):
    return [
        {"value": a, "shift": 0, "width": 8},
        {"value": b, "shift": 8, "width": 8},
        {"value": c, "shift": 16, "width": 16},
    ]


def CMD_HH(a, b):
    return [
        {"value": a, "shift": 0, "width": 16},
        {"value": b, "shift": 16, "width": 16},
    ]


def CMD_W(a):
    return [
        {"value": a, "shift": 0, "width": 32},
    ]


def CMD_PTR(a):
    return [
        {"value": a},
    ]


def define_geo_command(name: str, argnames: str, bits_12_15: int | None, *commands):
    args = []
    for argname in argnames.split(","):
        for index, command in enumerate(commands):
            for x in command:
                if isinstance(x["value"], str) and x["value"] == argname.strip():
                    args.append({
                        "index": index,
                        **x
                    })
    return {
        "name": name,
        "cmd": commands[0][0]["value"],
        "size": len(commands),
        "bits_12_15": bits_12_15,
        "args": args
    }


GEO_COMMANDS = [

define_geo_command(
    "GEO_BRANCH_AND_LINK",
    "scriptTarget",
    None,
        CMD_BBH(0x00, 0x00, 0x0000),
        CMD_PTR("scriptTarget")
),
define_geo_command(
    "GEO_END",
    "",
    None,
        CMD_BBH(0x01, 0x00, 0x0000)
),
define_geo_command(
    "GEO_BRANCH",
    "type, scriptTarget",
    None,
        CMD_BBH(0x02, "type", 0x0000),
        CMD_PTR("scriptTarget")
),
define_geo_command(
    "GEO_RETURN",
    "",
    None,
        CMD_BBH(0x03, 0x00, 0x0000)
),
define_geo_command(
    "GEO_OPEN_NODE",
    "",
    None,
        CMD_BBH(0x04, 0x00, 0x0000)
),
define_geo_command(
    "GEO_CLOSE_NODE",
    "",
    None,
        CMD_BBH(0x05, 0x00, 0x0000)
),
define_geo_command(
    "GEO_ASSIGN_AS_VIEW",
    "index",
    None,
        CMD_BBH(0x06, 0x00, "index")
),
define_geo_command(
    "GEO_UPDATE_NODE_FLAGS",
    "operation, flagBits",
    None,
        CMD_BBH(0x07, "operation", "flagBits")
),
define_geo_command(
    "GEO_NODE_SCREEN_AREA",
    "numEntries, x, y, width, height",
    None,
        CMD_BBH(0x08, 0x00, "numEntries"),
        CMD_HH("x", "y"),
        CMD_HH("width", "height")
),
define_geo_command(
    "GEO_NODE_ORTHO",
    "scale",
    None,
        CMD_BBH(0x09, 0x00, "scale")
),
define_geo_command(
    "GEO_CAMERA_FRUSTUM",
    "fov, near, far",
    None,
        CMD_BBH(0x0A, 0x00, "fov"),
        CMD_HH("near", "far")
),
define_geo_command(
    "GEO_CAMERA_FRUSTUM_WITH_FUNC",
    "fov, near, far, func",
    None,
        CMD_BBH(0x0A, 0x01, "fov"),
        CMD_HH("near", "far"),
        CMD_PTR("func")
),
define_geo_command(
    "GEO_NODE_START",
    "",
    None,
        CMD_BBH(0x0B, 0x00, 0x0000)
),
define_geo_command(
    "GEO_ZBUFFER",
    "enable",
    None,
        CMD_BBH(0x0C, "enable", 0x0000)
),
define_geo_command(
    "GEO_RENDER_RANGE",
    "minDistance, maxDistance",
    None,
        CMD_BBH(0x0D, 0x00, 0x0000),
        CMD_HH("minDistance", "maxDistance")
),
define_geo_command(
    "GEO_SWITCH_CASE",
    "param, function",
    None,
        CMD_BBH(0x0E, 0x00, "param"),
        CMD_PTR("function")
),
define_geo_command(
    "GEO_CAMERA",
    "cameraMode, x1, y1, z1, x2, y2, z2, function",
    None,
        CMD_BBH(0x0F, 0x00, "cameraMode"),
        CMD_HH("x1", "y1"),
        CMD_HH("z1", "x2"),
        CMD_HH("y2", "z2"),
        CMD_PTR("function")
),
define_geo_command(
    "GEO_TRANSLATE_ROTATE",
    "layer, tx, ty, tz, rx, ry, rz",
    0x0,
        CMD_BBH(0x10, "layer", 0x0000),
        CMD_HH("tx", "ty"),
        CMD_HH("tz", "rx"),
        CMD_HH("ry", "rz")
),
define_geo_command(
    "GEO_TRANSLATE_ROTATE_WITH_DL",
    "layer, tx, ty, tz, rx, ry, rz, displayList",
    0x8,
        CMD_BBH(0x10, "layer" , 0x0000),
        CMD_HH("tx", "ty"),
        CMD_HH("tz", "rx"),
        CMD_HH("ry", "rz"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_TRANSLATE",
    "layer, tx, ty, tz",
    0x1,
        CMD_BBH(0x10, "layer", "tx"),
        CMD_HH("ty", "tz")
),
define_geo_command(
    "GEO_TRANSLATE_WITH_DL",
    "layer, tx, ty, tz, displayList",
    0x9,
        CMD_BBH(0x10, "layer", "tx"),
        CMD_HH("ty", "tz"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_ROTATE",
    "layer, rx, ry, rz",
    0x2,
        CMD_BBH(0x10, "layer", "rx"),
        CMD_HH("ry", "rz")
),
define_geo_command(
    "GEO_ROTATE_WITH_DL",
    "layer, rx, ry, rz, displayList",
    0xA,
        CMD_BBH(0x10, "layer", "rx"),
        CMD_HH("ry", "rz"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_ROTATE_Y",
    "layer, ry",
    0x3,
        CMD_BBH(0x10, "layer", "ry")
),
define_geo_command(
    "GEO_ROTATE_Y_WITH_DL",
    "layer, ry, displayList",
    0xB,
        CMD_BBH(0x10, "layer", "ry"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_TRANSLATE_NODE",
    "layer, ux, uy, uz",
    0x0,
        CMD_BBH(0x11, "layer", "ux"),
        CMD_HH("uy", "uz")
),
define_geo_command(
    "GEO_TRANSLATE_NODE_WITH_DL",
    "layer, ux, uy, uz, displayList",
    0x8,
        CMD_BBH(0x11, "layer", "ux"),
        CMD_HH("uy", "uz"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_ROTATION_NODE",
    "layer, ux, uy, uz",
    0x0,
        CMD_BBH(0x12, "layer", "ux"),
        CMD_HH("uy", "uz")
),
define_geo_command(
    "GEO_ROTATION_NODE_WITH_DL",
    "layer, ux, uy, uz, displayList",
    0x8,
        CMD_BBH(0x12, "layer", "ux"),
        CMD_HH("uy", "uz"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_ANIMATED_PART",
    "layer, x, y, z, displayList",
    None,
        CMD_BBH(0x13, "layer", "x"),
        CMD_HH("y", "z"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_BILLBOARD_WITH_PARAMS",
    "layer, tx, ty, tz",
    0x0,
        CMD_BBH(0x14, "layer", "tx"),
        CMD_HH("ty", "tz")
),
define_geo_command(
    "GEO_BILLBOARD_WITH_PARAMS_AND_DL",
    "layer, tx, ty, tz, displayList",
    0x8,
        CMD_BBH(0x14, "layer", "tx"),
        CMD_HH("ty", "tz"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_DISPLAY_LIST",
    "layer, displayList",
    None,
        CMD_BBH(0x15, "layer", 0x0000),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_SHADOW",
    "shadowType, solidity, scale",
    None,
        CMD_BBH(0x16, 0x00, "shadowType"),
        CMD_HH("solidity", "scale")
),
define_geo_command(
    "GEO_RENDER_OBJ",
    "",
    None,
        CMD_BBH(0x17, 0x00, 0x0000)
),
define_geo_command(
    "GEO_ASM",
    "param, function",
    None,
        CMD_BBH(0x18, 0x00, "param"),
        CMD_PTR("function")
),
define_geo_command(
    "GEO_BACKGROUND",
    "background, function",
    None,
        CMD_BBH(0x19, 0x00, "background"),
        CMD_PTR("function")
),
define_geo_command(
    "GEO_NOP_1A",
    "",
    None,
        CMD_BBH(0x1A, 0x00, 0x0000),
        CMD_HH(0x0000, 0x0000)
),
define_geo_command(
    "GEO_COPY_VIEW",
    "index",
    None,
        CMD_BBH(0x1B, 0x00, "index")
),
define_geo_command(
    "GEO_HELD_OBJECT",
    "param, ux, uy, uz, nodeFunc",
    None,
        CMD_BBH(0x1C, "param", "ux"),
        CMD_HH("uy", "uz"),
        CMD_PTR("nodeFunc")
),
define_geo_command(
    "GEO_SCALE",
    "layer, scale",
    0x0,
        CMD_BBH(0x1D, "layer", 0x0000),
        CMD_W("scale")
),
define_geo_command(
    "GEO_SCALE_WITH_DL",
    "layer, scale, displayList",
    0x8,
        CMD_BBH(0x1D, "layer", 0x0000),
        CMD_W("scale"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_NOP_1E",
    "",
    None,
        CMD_BBH(0x1E, 0x00, 0x0000),
        CMD_HH(0x0000, 0x0000)
),
define_geo_command(
    "GEO_NOP_1F",
    "",
    None,
        CMD_BBH(0x1F, 0x00, 0x0000),
        CMD_HH(0x0000, 0x0000),
        CMD_HH(0x0000, 0x0000),
        CMD_HH(0x0000, 0x0000)
),
define_geo_command(
    "GEO_CULLING_RADIUS",
    "cullingRadius",
    None,
        CMD_BBH(0x20, 0x00, "cullingRadius")
),
define_geo_command(
    "GEO_BACKGROUND", # GEO_BACKGROUND_EXT
    "backgroundPtr, function",
    None,
        CMD_BBH(0x21, 0x00, 0x00),
        CMD_PTR("backgroundPtr"),
        CMD_PTR("function")
),
define_geo_command(
    "GEO_SWITCH_CASE", # GEO_SWITCH_CASE_EXT
    "param, function",
    None,
        CMD_BBH(0x22, 0x00, "param"),
        CMD_PTR("function")
),
define_geo_command(
    "GEO_ASM", # GEO_ASM_EXT
    "param, function",
    None,
        CMD_BBH(0x23, 0x00, "param"),
        CMD_PTR("function")
),

]


def write_geo_inc_c(dirpath: str, gfxdata: GfxData):
    with open(os.path.join(dirpath, "geo.inc.c"), "w", newline="\n") as geo_inc_c:
        for name, geolayout in gfxdata.geolayouts.items():
            geo_inc_c.write("GeoLayout %s[] = {\n" % (name))
            level = 1
            index = 0
            buffer = geolayout.buffer
            while index < len(buffer):
                cmd = (buffer[index] & 0xFF)
                bits_12_15 = (buffer[index] & 0xF000)
                for geo_command in GEO_COMMANDS:
                    if geo_command["cmd"] == cmd and (geo_command["bits_12_15"] is None or geo_command["bits_12_15"] == bits_12_15):
                        level -= (cmd == 0x05)
                        geo_inc_c.write("    " * level)
                        geo_inc_c.write(geo_command["name"] + "(")
                        args_str = ""
                        for arg in geo_command["args"]:
                            value = buffer[index + arg["index"]]
                            if "shift" in arg:
                                shift = arg["shift"]
                                width = arg["width"]
                                limit = (1 << width)
                                half = (limit >> 1)
                                value = ((value >> shift) & (limit - 1))
                                value = value if value < half else value - limit
                                value_str = "%d" % (value)
                            else:
                                value_str = str(value)

                            # replace constant by its name
                            arg_name = arg["value"]
                            if arg_name in GEO_CONSTANTS:
                                value_str = GEO_CONSTANTS[arg_name][value_str]

                            args_str += value_str + ", "
                        geo_inc_c.write((args_str[:-2] if args_str else "") + "),\n")
                        level += (cmd == 0x04)
                        index += geo_command["size"]
                        break
                else:
                    print(geo_command["cmd"])
            geo_inc_c.write("};\n\n")
