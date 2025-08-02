from .. import prints
from ..consts.bhv import BEHAVIOR_IDS
from ..consts.objects import OBJECT_FIELDS, OBJECT_FLAGS
from ..consts.models import MODEL_IDS
from ..gfxdata import GfxData
from .values import define_command, value_to_str, get_named_flags


INTERACT_TYPES = {
    (1 <<  0): "INTERACT_HOOT",
    (1 <<  1): "INTERACT_GRABBABLE",
    (1 <<  2): "INTERACT_DOOR",
    (1 <<  3): "INTERACT_DAMAGE",
    (1 <<  4): "INTERACT_COIN",
    (1 <<  5): "INTERACT_CAP",
    (1 <<  6): "INTERACT_POLE",
    (1 <<  7): "INTERACT_KOOPA",
    (1 <<  8): "INTERACT_SPINY_WALKING",
    (1 <<  9): "INTERACT_BREAKABLE",
    (1 << 10): "INTERACT_STRONG_WIND",
    (1 << 11): "INTERACT_WARP_DOOR",
    (1 << 12): "INTERACT_STAR_OR_KEY",
    (1 << 13): "INTERACT_WARP",
    (1 << 14): "INTERACT_CANNON_BASE",
    (1 << 15): "INTERACT_BOUNCE_TOP",
    (1 << 16): "INTERACT_WATER_RING",
    (1 << 17): "INTERACT_BULLY",
    (1 << 18): "INTERACT_FLAME",
    (1 << 19): "INTERACT_KOOPA_SHELL",
    (1 << 20): "INTERACT_BOUNCE_TOP2",
    (1 << 21): "INTERACT_MR_BLIZZARD",
    (1 << 22): "INTERACT_HIT_FROM_BELOW",
    (1 << 23): "INTERACT_TEXT",
    (1 << 24): "INTERACT_TORNADO",
    (1 << 25): "INTERACT_WHIRLPOOL",
    (1 << 26): "INTERACT_CLAM_OR_BUBBA",
    (1 << 27): "INTERACT_BBH_ENTRANCE",
    (1 << 28): "INTERACT_SNUFIT_BULLET",
    (1 << 29): "INTERACT_SHOCK",
    (1 << 30): "INTERACT_IGLOO_BARRIER",
    (1 << 31): "INTERACT_PLAYER",
}

INTERACT_SUBTYPES = {
    0x00000001: "INT_SUBTYPE_FADING_WARP",
    0x00000002: "INT_SUBTYPE_DELAY_INVINCIBILITY",
    0x00000008: "INT_SUBTYPE_BIG_KNOCKBACK",
    0x00000004: "INT_SUBTYPE_GRABS_MARIO",
    0x00000010: "INT_SUBTYPE_HOLDABLE_NPC",
    0x00000040: "INT_SUBTYPE_DROP_IMMEDIATELY",
    0x00000100: "INT_SUBTYPE_KICKABLE",
    0x00000200: "INT_SUBTYPE_NOT_GRABBABLE",
    0x00000020: "INT_SUBTYPE_STAR_DOOR",
    0x00000080: "INT_SUBTYPE_TWIRL_BOUNCE",
    0x00000400: "INT_SUBTYPE_NO_EXIT",
    0x00000800: "INT_SUBTYPE_GRAND_STAR",
    0x00001000: "INT_SUBTYPE_SIGN",
    0x00004000: "INT_SUBTYPE_NPC",
    0x00002000: "INT_SUBTYPE_EATS_MARIO",
}

ACTIVE_PARTICLES = {
    (1 <<  0): "ACTIVE_PARTICLE_DUST",
    (1 <<  1): "ACTIVE_PARTICLE_UNUSED_1",
    (1 <<  2): "ACTIVE_PARTICLE_UNUSED_2",
    (1 <<  3): "ACTIVE_PARTICLE_SPARKLES",
    (1 <<  4): "ACTIVE_PARTICLE_H_STAR",
    (1 <<  5): "ACTIVE_PARTICLE_BUBBLE",
    (1 <<  6): "ACTIVE_PARTICLE_WATER_SPLASH",
    (1 <<  7): "ACTIVE_PARTICLE_IDLE_WATER_WAVE",
    (1 <<  8): "ACTIVE_PARTICLE_SHALLOW_WATER_WAVE",
    (1 <<  9): "ACTIVE_PARTICLE_PLUNGE_BUBBLE",
    (1 << 10): "ACTIVE_PARTICLE_WAVE_TRAIL",
    (1 << 11): "ACTIVE_PARTICLE_FIRE",
    (1 << 12): "ACTIVE_PARTICLE_SHALLOW_WATER_SPLASH",
    (1 << 13): "ACTIVE_PARTICLE_LEAF",
    (1 << 14): "ACTIVE_PARTICLE_DIRT",
    (1 << 15): "ACTIVE_PARTICLE_MIST_CIRCLE",
    (1 << 16): "ACTIVE_PARTICLE_SNOW",
    (1 << 17): "ACTIVE_PARTICLE_BREATH",
    (1 << 18): "ACTIVE_PARTICLE_V_STAR",
    (1 << 19): "ACTIVE_PARTICLE_TRIANGLE",
}

BEHAVIOR_CONSTANTS = {
    "objList": {
        "0": "OBJ_LIST_PLAYER",
        "1": "OBJ_LIST_EXT",
        "2": "OBJ_LIST_DESTRUCTIVE",
        "3": "OBJ_LIST_UNUSED_3",
        "4": "OBJ_LIST_GENACTOR",
        "5": "OBJ_LIST_PUSHABLE",
        "6": "OBJ_LIST_LEVEL",
        "7": "OBJ_LIST_UNUSED_7",
        "8": "OBJ_LIST_DEFAULT",
        "9": "OBJ_LIST_SURFACE",
        "10": "OBJ_LIST_POLELIKE",
        "11": "OBJ_LIST_SPAWNER",
        "12": "OBJ_LIST_UNIMPORTANT",
    },
    "id": {
        "65535": "id_bhvNewId",
    **{
        str(i): name
        for i, name in enumerate(BEHAVIOR_IDS)
    }},
    "field": {
        ("0x%X" % (i)): name
        for i, name in OBJECT_FIELDS.items()
    },
    "field1": {
        ("0x%X" % (i)): name
        for i, name in OBJECT_FIELDS.items()
    },
    "field2": {
        ("0x%X" % (i)): name
        for i, name in OBJECT_FIELDS.items()
    },
    "modelID": {
        ("0x%X" % (i)): name
        for i, name in MODEL_IDS.items()
    },
    "interactType": {
        ("0x%X" % (i)): name
        for i, name in INTERACT_TYPES.items()
    },
    "interactSubtype": {
        ("0x%X" % (i)): name
        for i, name in INTERACT_SUBTYPES.items()
    },
}


def BC_B(a):
    return [
        {"value": a, "shift": 24, "width": 8},
    ]

def BC_BB(a, b):
    return [
        {"value": a, "shift": 24, "width": 8},
        {"value": b, "shift": 16, "width": 8},
    ]

def BC_BBBB(a, b, c, d):
    return [
        {"value": a, "shift": 24, "width": 8},
        {"value": b, "shift": 16, "width": 8},
        {"value": c, "shift": 8, "width": 8},
        {"value": d, "shift": 0, "width": 8},
    ]

def BC_BBH(a, b, c):
    return [
        {"value": a, "shift": 24, "width": 8},
        {"value": b, "shift": 16, "width": 8},
        {"value": c, "shift": 0, "width": 16},
    ]

def BC_B0H(a, b):
    return [
        {"value": a, "shift": 24, "width": 8},
        {"value": b, "shift": 0, "width": 16},
    ]

def BC_H(a):
    return [
        {"value": a, "shift": 16, "width": 16},
    ]

def BC_HH(a, b):
    return [
        {"value": a, "shift": 16, "width": 16},
        {"value": b, "shift": 0, "width": 16},
    ]

def BC_W(a):
    return [
        {"value": a, "shift": 0, "width": 32},
    ]

def BC_PTR(a):
    return [
        {"value": a},
    ]


BEHAVIOR_COMMANDS = [

define_command(
    "BEGIN",
    "objList",
        BC_BB(0x00, "objList")
),
define_command(
    "DELAY",
    "num",
        BC_B0H(0x01, "num:u")
),
define_command(
    "CALL",
    "addr",
        BC_B(0x02),
        BC_PTR("addr")
),
define_command(
    "RETURN",
    "",
        BC_B(0x03)
),
define_command(
    "GOTO",
    "addr",
        BC_B(0x04),
        BC_PTR("addr")
),
define_command(
    "BEGIN_REPEAT",
    "count",
        BC_B0H(0x05, "count:u")
),
define_command(
    "END_REPEAT",
    "",
        BC_B(0x06)
),
define_command(
    "END_REPEAT_CONTINUE",
    "",
        BC_B(0x07)
),
define_command(
    "BEGIN_LOOP",
    "",
        BC_B(0x08)
),
define_command(
    "END_LOOP",
    "",
        BC_B(0x09)
),
define_command(
    "BREAK",
    "",
        BC_B(0x0A)
),
define_command(
    "BREAK_UNUSED",
    "",
        BC_B(0x0B)
),
define_command(
    "CALL_NATIVE",
    "func",
        BC_B(0x0C),
        BC_PTR("func")
),
define_command(
    "ADD_FLOAT",
    "field, value",
        BC_BBH(0x0D, "field:x", "value:s")
),
define_command(
    "SET_FLOAT",
    "field, value",
        BC_BBH(0x0E, "field:x", "value:s")
),
define_command(
    "ADD_INT",
    "field, value",
        BC_BBH(0x0F, "field:x", "value:s")
),
define_command(
    "SET_INT",
    "field, value",
        BC_BBH(0x10, "field:x", "value:s")
),
define_command(
    "OR_INT",
    "field, value",
        BC_BBH(0x11, "field:x", "value:s")
),
define_command(
    "BIT_CLEAR",
    "field, value",
        BC_BBH(0x12, "field:x", "value:x")
),
define_command(
    "SET_INT_RAND_RSHIFT",
    "field, min, rshift",
        BC_BBH(0x13, "field:x", "min:s"),
        BC_H("rshift:u")
),
define_command(
    "SET_RANDOM_FLOAT",
    "field, min, range",
        BC_BBH(0x14, "field:x", "min:s"),
        BC_H("range:u")
),
define_command(
    "SET_RANDOM_INT",
    "field, min, range",
        BC_BBH(0x15, "field:x", "min:s"),
        BC_H("range:u")
),
define_command(
    "ADD_RANDOM_FLOAT",
    "field, min, range",
        BC_BBH(0x16, "field:x", "min:s"),
        BC_H("range:u")
),
define_command(
    "ADD_INT_RAND_RSHIFT",
    "field, min, rshift",
        BC_BBH(0x17, "field:x", "min:s"),
        BC_H("rshift:u")
),
define_command(
    "CMD_NOP_1",
    "field",
        BC_BB(0x18, "field:x")
),
define_command(
    "CMD_NOP_2",
    "field",
        BC_BB(0x19, "field:x")
),
define_command(
    "CMD_NOP_3",
    "field",
        BC_BB(0x1A, "field:x")
),
define_command(
    "SET_MODEL",
    "modelID",
        BC_B0H(0x1B, "modelID:x")
),
define_command(
    "SPAWN_CHILD",
    "modelID, behavior",
        BC_B(0x1C),
        BC_W("modelID:x"),
        BC_PTR("behavior")
),
define_command(
    "DEACTIVATE",
    "",
        BC_B(0x1D)
),
define_command(
    "DROP_TO_FLOOR",
    "",
        BC_B(0x1E)
),
define_command(
    "SUM_FLOAT",
    "field, field1, field2",
        BC_BBBB(0x1F, "field:x", "field1:x", "field2:x")
),
define_command(
    "SUM_INT",
    "field, field1, field2",
        BC_BBBB(0x20, "field:x", "field1:x", "field2:x")
),
define_command(
    "BILLBOARD",
    "",
        BC_B(0x21)
),
define_command(
    "CYLBOARD",
    "",
        BC_B(0x38)
),
define_command(
    "HIDE",
    "",
        BC_B(0x22)
),
define_command(
    "SET_HITBOX",
    "radius, height",
        BC_B(0x23),
        BC_HH("radius:u", "height:u")
),
define_command(
    "CMD_NOP_4",
    "field, value",
        BC_BBH(0x24, "field:x", "value")
),
define_command(
    "DELAY_VAR",
    "field",
        BC_BB(0x25, "field:x")
),
define_command(
    "BEGIN_REPEAT_UNUSED",
    "count",
        BC_BB(0x26, "count:u")
),
define_command(
    "LOAD_ANIMATIONS",
    "field, anims",
        BC_BB(0x27, "field:x"),
        BC_PTR("anims")
),
define_command(
    "ANIMATE",
    "animIndex",
        BC_BB(0x28, "animIndex")
),
define_command(
    "SPAWN_CHILD_WITH_PARAM",
    "bhvParam, modelID, behavior",
        BC_B0H(0x29, "bhvParam:u"),
        BC_W("modelID:x"),
        BC_PTR("behavior")
),
define_command(
    "LOAD_COLLISION_DATA",
    "collisionData",
        BC_B(0x2A),
        BC_PTR("collisionData")
),
define_command(
    "SET_HITBOX_WITH_OFFSET",
    "radius, height, downOffset",
        BC_B(0x2B),
        BC_HH("radius:u", "height:u"),
        BC_H("downOffset:u")
),
define_command(
    "SPAWN_OBJ",
    "modelID, behavior",
        BC_B(0x2C),
        BC_W("modelID:x"),
        BC_PTR("behavior")
),
define_command(
    "SET_HOME",
    "",
        BC_B(0x2D)
),
define_command(
    "SET_HURTBOX",
    "radius, height",
        BC_B(0x2E),
        BC_HH("radius:u", "height:u")
),
define_command(
    "SET_INTERACT_TYPE",
    "interactType",
        BC_B(0x2F),
        BC_W("interactType:x")
),
define_command(
    "SET_OBJ_PHYSICS",
    "wallHitboxRadius, gravity, bounciness, dragStrength, friction, buoyancy, unused1, unused2",
        BC_B(0x30),
        BC_HH("wallHitboxRadius:u", "gravity:s"),
        BC_HH("bounciness:s", "dragStrength:u"),
        BC_HH("friction:u", "buoyancy:u"),
        BC_HH("unused1:u", "unused2:u")
),
define_command(
    "SET_INTERACT_SUBTYPE",
    "interactSubtype",
        BC_B(0x31),
        BC_W("interactSubtype:x")
),
define_command(
    "SCALE",
    "unused, percent",
        BC_BBH(0x32, "unused", "percent:u")
),
define_command(
    "PARENT_BIT_CLEAR",
    "field, value",
        BC_BB(0x33, "field:x"),
        BC_W("value:x")
),
define_command(
    "ANIMATE_TEXTURE",
    "field, rate",
        BC_BBH(0x34, "field:x", "rate:u")
),
define_command(
    "DISABLE_RENDERING",
    "",
        BC_B(0x35)
),
define_command(
    "SET_INT_UNUSED",
    "field, value",
        BC_BB(0x36, "field:x"),
        BC_HH(0, "value:u")
),
# define_command(
#     "SPAWN_WATER_DROPLET",
#     "dropletParams",
#         BC_B(0x37),
#         BC_PTR("dropletParams")
# ),
define_command(
    "ID",
    "id",
        BC_B0H(0x39, "id")
),
define_command(
    "CALL",
    "addr",
        BC_B(0x3A),
        BC_PTR("addr")
),
define_command(
    "GOTO",
    "addr",
        BC_B(0x3B),
        BC_PTR("addr")
),
define_command(
    "CALL_NATIVE",
    "func",
        BC_B(0x3C),
        BC_PTR("func")
),
define_command(
    "SPAWN_CHILD",
    "modelID, behavior",
        BC_B(0x3D),
        BC_W("modelID:x"),
        BC_PTR("behavior")
),
define_command(
    "SPAWN_CHILD_WITH_PARAM",
    "bhvParam, modelID, behavior",
        BC_B0H(0x3E, "bhvParam:u"),
        BC_W("modelID:x"),
        BC_PTR("behavior")
),
define_command(
    "SPAWN_OBJ",
    "modelID, behavior",
        BC_B(0x3F),
        BC_W("modelID:x"),
        BC_PTR("behavior")
),
define_command(
    "LOAD_ANIMATIONS",
    "field, anims",
        BC_BB(0x40, "field:x"),
        BC_PTR("anims")
),
define_command(
    "LOAD_COLLISION_DATA",
    "collisionData",
        BC_B(0x41),
        BC_PTR("collisionData")
),
# define_command(
#     "CALL_LUA_FUNC",
#     "func",
#         BC_B(0x42),
#         BC_W("func")
# ),

]

BEHAVIOR_COMMANDS_LEVELS = {
    "BEGIN_LOOP": +1,
    "END_LOOP": -1,
    "BEGIN_REPEAT": +1,
    "END_REPEAT": -1,
}

BEHAVIOR_VALUES = {
    "oFlags": lambda flags: get_named_flags(flags, OBJECT_FLAGS),
    "oInteractType": lambda interactType: INTERACT_TYPES[interactType],
    "oInteractionSubtype": lambda interactSubtypes: get_named_flags(interactSubtypes, INTERACT_SUBTYPES),
    "oActiveParticleFlags": lambda flags: get_named_flags(flags, ACTIVE_PARTICLES),
}


@GfxData.writer()
def write_behavior_data_c(self: GfxData, behavior_data_filepath: str, append_mode: bool):
    with open(behavior_data_filepath, "a" if append_mode else "w", newline="\n") as behavior_data_c:
        for name, behavior in self.behaviors.items():
            behavior_data_c.write("const BehaviorScript %s[] = {\n" % (name))
            level = 1
            index = 0
            buffer = behavior.buffer
            while index < len(buffer):
                cmd = ((buffer[index] >> 24) & 0xFF)
                for bhv_command in BEHAVIOR_COMMANDS:
                    if bhv_command["cmd"] == cmd:
                        level += min(0, BEHAVIOR_COMMANDS_LEVELS.get(bhv_command["name"], 0))
                        behavior_data_c.write("    " * level)
                        behavior_data_c.write(bhv_command["name"] + "(")
                        args_str = ""
                        field = None
                        for arg in bhv_command["args"]:
                            value = buffer[index + arg["index"]]
                            if "shift" in arg:
                                value_str = value_to_str(value, arg["shift"], arg["width"], arg["type"])
                            else:
                                value_str = str(value)

                            # replace constant by its name
                            arg_name = arg["value"]
                            if arg_name in BEHAVIOR_CONSTANTS:
                                if value_str in BEHAVIOR_CONSTANTS[arg_name]:
                                    value_str = BEHAVIOR_CONSTANTS[arg_name][value_str]
                                else:
                                    prints.warning("Unknown value for '%s': %s" % (arg_name, value_str))

                            # 'field' param
                            if arg_name == "field":
                                field = value_str
                            elif arg_name == "value" and field is not None and field in BEHAVIOR_VALUES:
                                value = int(value_str[2:], 16) if value_str.startswith("0x") else int(value_str)
                                value_str = BEHAVIOR_VALUES[field](value)

                            args_str += value_str + ", "
                        behavior_data_c.write((args_str[:-2] if args_str else "") + "),\n")
                        level += max(0, BEHAVIOR_COMMANDS_LEVELS.get(bhv_command["name"], 0))
                        index += bhv_command["size"]
                        break
                else:
                    prints.warning("Unknown behavior command: 0x%02X" % (cmd))
                    break
            behavior_data_c.write("};\n\n")
