import os
from .. import prints
from ..gfxdata import GfxData


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
        "51": "SHADOW_RECTANGLE_HARDCODED_OFFSET+1", # Whomp
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


def define_geo_command(name: str, argnames: str, bits_12_15: int|None, *commands):
    args = []
    for argname in argnames.split(","):
        for index, command in enumerate(commands):
            for x in command:
                if isinstance(x["value"], str):
                    xname = x["value"]
                    xtype = "u"
                    sep = xname.find(":")
                    if sep != -1:
                        xtype = xname[sep+1:]
                        xname = xname[:sep]
                    if xname == argname.strip():
                        args.append({
                            "index": index,
                            "value": xname,
                            "type": xtype,
                            **{ k: v for k, v in x.items() if k != "value" }
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
        CMD_BBH(0x02, "type:u", 0x0000),
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
        CMD_BBH(0x06, 0x00, "index:u")
),
define_geo_command(
    "GEO_UPDATE_NODE_FLAGS",
    "operation, flagBits",
    None,
        CMD_BBH(0x07, "operation:u", "flagBits:x")
),
define_geo_command(
    "GEO_NODE_SCREEN_AREA",
    "numEntries, x, y, width, height",
    None,
        CMD_BBH(0x08, 0x00, "numEntries:u"),
        CMD_HH("x:s", "y:s"),
        CMD_HH("width:u", "height:u")
),
define_geo_command(
    "GEO_NODE_ORTHO",
    "scale",
    None,
        CMD_BBH(0x09, 0x00, "scale:u")
),
define_geo_command(
    "GEO_CAMERA_FRUSTUM",
    "fov, near, far",
    None,
        CMD_BBH(0x0A, 0x00, "fov:u"),
        CMD_HH("near:u", "far:u")
),
define_geo_command(
    "GEO_CAMERA_FRUSTUM_WITH_FUNC",
    "fov, near, far, func",
    None,
        CMD_BBH(0x0A, 0x01, "fov:u"),
        CMD_HH("near:u", "far:u"),
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
        CMD_BBH(0x0C, "enable:u", 0x0000)
),
define_geo_command(
    "GEO_RENDER_RANGE",
    "minDistance, maxDistance",
    None,
        CMD_BBH(0x0D, 0x00, 0x0000),
        CMD_HH("minDistance:s", "maxDistance:s")
),
define_geo_command(
    "GEO_SWITCH_CASE",
    "param, function",
    None,
        CMD_BBH(0x0E, 0x00, "param:u"),
        CMD_PTR("function")
),
define_geo_command(
    "GEO_CAMERA",
    "cameraMode, x1, y1, z1, x2, y2, z2, function",
    None,
        CMD_BBH(0x0F, 0x00, "cameraMode:u"),
        CMD_HH("x1:s", "y1:s"),
        CMD_HH("z1:s", "x2:s"),
        CMD_HH("y2:s", "z2:s"),
        CMD_PTR("function")
),
define_geo_command(
    "GEO_TRANSLATE_ROTATE",
    "layer, tx, ty, tz, rx, ry, rz",
    0x0,
        CMD_BBH(0x10, "layer:u", 0x0000),
        CMD_HH("tx:s", "ty:s"),
        CMD_HH("tz:s", "rx:s"),
        CMD_HH("ry:s", "rz:s")
),
define_geo_command(
    "GEO_TRANSLATE_ROTATE_WITH_DL",
    "layer, tx, ty, tz, rx, ry, rz, displayList",
    0x8,
        CMD_BBH(0x10, "layer:u" , 0x0000),
        CMD_HH("tx:s", "ty:s"),
        CMD_HH("tz:s", "rx:s"),
        CMD_HH("ry:s", "rz:s"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_TRANSLATE",
    "layer, tx, ty, tz",
    0x1,
        CMD_BBH(0x10, "layer:u", "tx:s"),
        CMD_HH("ty:s", "tz:s")
),
define_geo_command(
    "GEO_TRANSLATE_WITH_DL",
    "layer, tx, ty, tz, displayList",
    0x9,
        CMD_BBH(0x10, "layer:u", "tx:s"),
        CMD_HH("ty:s", "tz:s"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_ROTATE",
    "layer, rx, ry, rz",
    0x2,
        CMD_BBH(0x10, "layer:u", "rx:s"),
        CMD_HH("ry:s", "rz:s")
),
define_geo_command(
    "GEO_ROTATE_WITH_DL",
    "layer, rx, ry, rz, displayList",
    0xA,
        CMD_BBH(0x10, "layer:u", "rx:s"),
        CMD_HH("ry:s", "rz:s"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_ROTATE_Y",
    "layer, ry",
    0x3,
        CMD_BBH(0x10, "layer:u", "ry:s")
),
define_geo_command(
    "GEO_ROTATE_Y_WITH_DL",
    "layer, ry, displayList",
    0xB,
        CMD_BBH(0x10, "layer:u", "ry:s"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_TRANSLATE_NODE",
    "layer, ux, uy, uz",
    0x0,
        CMD_BBH(0x11, "layer:u", "ux:s"),
        CMD_HH("uy:s", "uz:s")
),
define_geo_command(
    "GEO_TRANSLATE_NODE_WITH_DL",
    "layer, ux, uy, uz, displayList",
    0x8,
        CMD_BBH(0x11, "layer:u", "ux:s"),
        CMD_HH("uy:s", "uz:s"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_ROTATION_NODE",
    "layer, ux, uy, uz",
    0x0,
        CMD_BBH(0x12, "layer:u", "ux:s"),
        CMD_HH("uy:s", "uz:s")
),
define_geo_command(
    "GEO_ROTATION_NODE_WITH_DL",
    "layer, ux, uy, uz, displayList",
    0x8,
        CMD_BBH(0x12, "layer:u", "ux:s"),
        CMD_HH("uy:s", "uz:s"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_ANIMATED_PART",
    "layer, x, y, z, displayList",
    None,
        CMD_BBH(0x13, "layer:u", "x:s"),
        CMD_HH("y:s", "z:s"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_BILLBOARD_WITH_PARAMS",
    "layer, tx, ty, tz",
    0x0,
        CMD_BBH(0x14, "layer:u", "tx:s"),
        CMD_HH("ty:s", "tz:s")
),
define_geo_command(
    "GEO_BILLBOARD_WITH_PARAMS_AND_DL",
    "layer, tx, ty, tz, displayList",
    0x8,
        CMD_BBH(0x14, "layer:u", "tx:s"),
        CMD_HH("ty:s", "tz:s"),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_DISPLAY_LIST",
    "layer, displayList",
    None,
        CMD_BBH(0x15, "layer:u", 0x0000),
        CMD_PTR("displayList")
),
define_geo_command(
    "GEO_SHADOW",
    "shadowType, solidity, scale",
    None,
        CMD_BBH(0x16, 0x00, "shadowType:u"),
        CMD_HH("solidity:u", "scale:u")
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
        CMD_BBH(0x18, 0x00, "param:u"),
        CMD_PTR("function")
),
define_geo_command(
    "GEO_BACKGROUND",
    "background, function",
    None,
        CMD_BBH(0x19, 0x00, "background:u"),
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
        CMD_BBH(0x1B, 0x00, "index:u")
),
define_geo_command(
    "GEO_HELD_OBJECT",
    "param, ux, uy, uz, nodeFunc",
    None,
        CMD_BBH(0x1C, "param:u", "ux:s"),
        CMD_HH("uy:s", "uz:s"),
        CMD_PTR("nodeFunc")
),
define_geo_command(
    "GEO_SCALE",
    "layer, scale",
    0x0,
        CMD_BBH(0x1D, "layer:u", 0x0000),
        CMD_W("scale:x")
),
define_geo_command(
    "GEO_SCALE_WITH_DL",
    "layer, scale, displayList",
    0x8,
        CMD_BBH(0x1D, "layer:u", 0x0000),
        CMD_W("scale:x"),
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
        CMD_BBH(0x20, 0x00, "cullingRadius:u")
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
        CMD_BBH(0x22, 0x00, "param:u"),
        CMD_PTR("function")
),
define_geo_command(
    "GEO_ASM", # GEO_ASM_EXT
    "param, function",
    None,
        CMD_BBH(0x23, 0x00, "param:u"),
        CMD_PTR("function")
),

]


def value_to_str(value: int, shift: int, width: int, argtype: str):
    limit = (1 << width)
    value = ((value >> shift) & (limit - 1))

    # Signed value
    if argtype == "s":
        half = (limit >> 1)
        value = value if value < half else value - limit

    # (Hexa)decimal
    return ("0x%X" if argtype == "x" else "%d") % (value)


@GfxData.writer()
def write_geo_inc_c(self: GfxData, dirpath: str):
    with open(os.path.join(dirpath, "geo.inc.c"), "w", newline="\n") as geo_inc_c:
        for name, geolayout in self.geolayouts.items():
            geo_inc_c.write("GeoLayout %s[] = {\n" % (name))
            level = 1
            index = 0
            buffer = geolayout.buffer
            while index < len(buffer):
                cmd = (buffer[index] & 0xFF)
                bits_12_15 = (buffer[index] & 0xF000) >> 12
                for geo_command in GEO_COMMANDS:
                    if geo_command["cmd"] == cmd and (geo_command["bits_12_15"] is None or geo_command["bits_12_15"] == bits_12_15):
                        level -= (cmd == 0x05)
                        geo_inc_c.write("    " * level)
                        geo_inc_c.write(geo_command["name"] + "(")
                        args_str = ""
                        for arg in geo_command["args"]:
                            value = buffer[index + arg["index"]]
                            if "shift" in arg:

                                # hacky fix for drawing layer
                                if geo_command["bits_12_15"] is not None and arg["value"] == "layer" and bits_12_15 & 0x8:
                                    arg["width"] = 4

                                value_str = value_to_str(value, arg["shift"], arg["width"], arg["type"])
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
                    prints.warning("Unknown geo command: 0x%02X (bits_12_15: 0x%01X)" % (cmd, bits_12_15))
                    break
            geo_inc_c.write("};\n\n")
