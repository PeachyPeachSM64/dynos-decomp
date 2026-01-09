import os
from .. import prints
from ..gfxdata import GfxData
from .values import value_to_str


COLLISION_CONSTANTS = {
    "surfType": {
        0x0000: "SURFACE_DEFAULT",
        0x0001: "SURFACE_BURNING",
        0x0003: "SURFACE_RAYCAST",
        0x0004: "SURFACE_0004",
        0x0005: "SURFACE_HANGABLE",
        0x0009: "SURFACE_SLOW",
        0x000A: "SURFACE_DEATH_PLANE",
        0x000B: "SURFACE_CLOSE_CAMERA",
        0x000D: "SURFACE_WATER",
        0x000E: "SURFACE_FLOWING_WATER",
        0x0012: "SURFACE_INTANGIBLE",
        0x0013: "SURFACE_VERY_SLIPPERY",
        0x0014: "SURFACE_SLIPPERY",
        0x0015: "SURFACE_NOT_SLIPPERY",
        0x0016: "SURFACE_TTM_VINES",
        0x001A: "SURFACE_MGR_MUSIC",
        0x001B: "SURFACE_INSTANT_WARP_1B",
        0x001C: "SURFACE_INSTANT_WARP_1C",
        0x001D: "SURFACE_INSTANT_WARP_1D",
        0x001E: "SURFACE_INSTANT_WARP_1E",
        0x0021: "SURFACE_SHALLOW_QUICKSAND",
        0x0022: "SURFACE_DEEP_QUICKSAND",
        0x0023: "SURFACE_INSTANT_QUICKSAND",
        0x0024: "SURFACE_DEEP_MOVING_QUICKSAND",
        0x0025: "SURFACE_SHALLOW_MOVING_QUICKSAND",
        0x0026: "SURFACE_QUICKSAND",
        0x0027: "SURFACE_MOVING_QUICKSAND",
        0x0028: "SURFACE_WALL_MISC",
        0x0029: "SURFACE_NOISE_DEFAULT",
        0x002A: "SURFACE_NOISE_SLIPPERY",
        0x002C: "SURFACE_HORIZONTAL_WIND",
        0x002D: "SURFACE_INSTANT_MOVING_QUICKSAND",
        0x002E: "SURFACE_ICE",
        0x002F: "SURFACE_LOOK_UP_WARP",
        0x0030: "SURFACE_HARD",
        0x0032: "SURFACE_WARP",
        0x0033: "SURFACE_TIMER_START",
        0x0034: "SURFACE_TIMER_END",
        0x0035: "SURFACE_HARD_SLIPPERY",
        0x0036: "SURFACE_HARD_VERY_SLIPPERY",
        0x0037: "SURFACE_HARD_NOT_SLIPPERY",
        0x0038: "SURFACE_VERTICAL_WIND",
        0x0065: "SURFACE_BOSS_FIGHT_CAMERA",
        0x0066: "SURFACE_CAMERA_FREE_ROAM",
        0x0068: "SURFACE_THI3_WALLKICK",
        0x0069: "SURFACE_CAMERA_8_DIR",
        0x006E: "SURFACE_CAMERA_MIDDLE",
        0x006F: "SURFACE_CAMERA_ROTATE_RIGHT",
        0x0070: "SURFACE_CAMERA_ROTATE_LEFT",
        0x0072: "SURFACE_CAMERA_BOUNDARY",
        0x0073: "SURFACE_NOISE_VERY_SLIPPERY_73",
        0x0074: "SURFACE_NOISE_VERY_SLIPPERY_74",
        0x0075: "SURFACE_NOISE_VERY_SLIPPERY",
        0x0076: "SURFACE_NO_CAM_COLLISION",
        0x0077: "SURFACE_NO_CAM_COLLISION_77",
        0x0078: "SURFACE_NO_CAM_COL_VERY_SLIPPERY",
        0x0079: "SURFACE_NO_CAM_COL_SLIPPERY",
        0x007A: "SURFACE_SWITCH",
        0x007B: "SURFACE_VANISH_CAP_WALLS",
        0x00A6: "SURFACE_PAINTING_WOBBLE_A6",
        0x00A7: "SURFACE_PAINTING_WOBBLE_A7",
        0x00A8: "SURFACE_PAINTING_WOBBLE_A8",
        0x00A9: "SURFACE_PAINTING_WOBBLE_A9",
        0x00AA: "SURFACE_PAINTING_WOBBLE_AA",
        0x00AB: "SURFACE_PAINTING_WOBBLE_AB",
        0x00AC: "SURFACE_PAINTING_WOBBLE_AC",
        0x00AD: "SURFACE_PAINTING_WOBBLE_AD",
        0x00AE: "SURFACE_PAINTING_WOBBLE_AE",
        0x00AF: "SURFACE_PAINTING_WOBBLE_AF",
        0x00B0: "SURFACE_PAINTING_WOBBLE_B0",
        0x00B1: "SURFACE_PAINTING_WOBBLE_B1",
        0x00B2: "SURFACE_PAINTING_WOBBLE_B2",
        0x00B3: "SURFACE_PAINTING_WOBBLE_B3",
        0x00B4: "SURFACE_PAINTING_WOBBLE_B4",
        0x00B5: "SURFACE_PAINTING_WOBBLE_B5",
        0x00B6: "SURFACE_PAINTING_WOBBLE_B6",
        0x00B7: "SURFACE_PAINTING_WOBBLE_B7",
        0x00B8: "SURFACE_PAINTING_WOBBLE_B8",
        0x00B9: "SURFACE_PAINTING_WOBBLE_B9",
        0x00BA: "SURFACE_PAINTING_WOBBLE_BA",
        0x00BB: "SURFACE_PAINTING_WOBBLE_BB",
        0x00BC: "SURFACE_PAINTING_WOBBLE_BC",
        0x00BD: "SURFACE_PAINTING_WOBBLE_BD",
        0x00BE: "SURFACE_PAINTING_WOBBLE_BE",
        0x00BF: "SURFACE_PAINTING_WOBBLE_BF",
        0x00C0: "SURFACE_PAINTING_WOBBLE_C0",
        0x00C1: "SURFACE_PAINTING_WOBBLE_C1",
        0x00C2: "SURFACE_PAINTING_WOBBLE_C2",
        0x00C3: "SURFACE_PAINTING_WOBBLE_C3",
        0x00C4: "SURFACE_PAINTING_WOBBLE_C4",
        0x00C5: "SURFACE_PAINTING_WOBBLE_C5",
        0x00C6: "SURFACE_PAINTING_WOBBLE_C6",
        0x00C7: "SURFACE_PAINTING_WOBBLE_C7",
        0x00C8: "SURFACE_PAINTING_WOBBLE_C8",
        0x00C9: "SURFACE_PAINTING_WOBBLE_C9",
        0x00CA: "SURFACE_PAINTING_WOBBLE_CA",
        0x00CB: "SURFACE_PAINTING_WOBBLE_CB",
        0x00CC: "SURFACE_PAINTING_WOBBLE_CC",
        0x00CD: "SURFACE_PAINTING_WOBBLE_CD",
        0x00CE: "SURFACE_PAINTING_WOBBLE_CE",
        0x00CF: "SURFACE_PAINTING_WOBBLE_CF",
        0x00D0: "SURFACE_PAINTING_WOBBLE_D0",
        0x00D1: "SURFACE_PAINTING_WOBBLE_D1",
        0x00D2: "SURFACE_PAINTING_WOBBLE_D2",
        0x00D3: "SURFACE_PAINTING_WARP_D3",
        0x00D4: "SURFACE_PAINTING_WARP_D4",
        0x00D5: "SURFACE_PAINTING_WARP_D5",
        0x00D6: "SURFACE_PAINTING_WARP_D6",
        0x00D7: "SURFACE_PAINTING_WARP_D7",
        0x00D8: "SURFACE_PAINTING_WARP_D8",
        0x00D9: "SURFACE_PAINTING_WARP_D9",
        0x00DA: "SURFACE_PAINTING_WARP_DA",
        0x00DB: "SURFACE_PAINTING_WARP_DB",
        0x00DC: "SURFACE_PAINTING_WARP_DC",
        0x00DD: "SURFACE_PAINTING_WARP_DD",
        0x00DE: "SURFACE_PAINTING_WARP_DE",
        0x00DF: "SURFACE_PAINTING_WARP_DF",
        0x00E0: "SURFACE_PAINTING_WARP_E0",
        0x00E1: "SURFACE_PAINTING_WARP_E1",
        0x00E2: "SURFACE_PAINTING_WARP_E2",
        0x00E3: "SURFACE_PAINTING_WARP_E3",
        0x00E4: "SURFACE_PAINTING_WARP_E4",
        0x00E5: "SURFACE_PAINTING_WARP_E5",
        0x00E6: "SURFACE_PAINTING_WARP_E6",
        0x00E7: "SURFACE_PAINTING_WARP_E7",
        0x00E8: "SURFACE_PAINTING_WARP_E8",
        0x00E9: "SURFACE_PAINTING_WARP_E9",
        0x00EA: "SURFACE_PAINTING_WARP_EA",
        0x00EB: "SURFACE_PAINTING_WARP_EB",
        0x00EC: "SURFACE_PAINTING_WARP_EC",
        0x00ED: "SURFACE_PAINTING_WARP_ED",
        0x00EE: "SURFACE_PAINTING_WARP_EE",
        0x00EF: "SURFACE_PAINTING_WARP_EF",
        0x00F0: "SURFACE_PAINTING_WARP_F0",
        0x00F1: "SURFACE_PAINTING_WARP_F1",
        0x00F2: "SURFACE_PAINTING_WARP_F2",
        0x00F3: "SURFACE_PAINTING_WARP_F3",
        0x00F4: "SURFACE_TTC_PAINTING_1",
        0x00F5: "SURFACE_TTC_PAINTING_2",
        0x00F6: "SURFACE_TTC_PAINTING_3",
        0x00F7: "SURFACE_PAINTING_WARP_F7",
        0x00F8: "SURFACE_PAINTING_WARP_F8",
        0x00F9: "SURFACE_PAINTING_WARP_F9",
        0x00FA: "SURFACE_PAINTING_WARP_FA",
        0x00FB: "SURFACE_PAINTING_WARP_FB",
        0x00FC: "SURFACE_PAINTING_WARP_FC",
        0x00FD: "SURFACE_WOBBLING_WARP",
        0x00FF: "SURFACE_TRAPDOOR",
    },
    "preset": {
        0: "special_null_start",
        1: "special_yellow_coin",
        2: "special_yellow_coin_2",
        3: "special_unknown_3",
        4: "special_boo",
        5: "special_unknown_5",
        6: "special_lll_moving_octagonal_mesh_platform",
        7: "special_snow_ball",
        8: "special_lll_drawbridge_spawner",
        9: "special_empty_9",
        10: "special_lll_rotating_block_with_fire_bars",
        11: "special_lll_floating_wood_bridge",
        12: "special_tumbling_platform",
        13: "special_lll_rotating_hexagonal_ring",
        14: "special_lll_sinking_rectangular_platform",
        15: "special_lll_sinking_square_platforms",
        16: "special_lll_tilting_square_platform",
        17: "special_lll_bowser_puzzle",
        18: "special_mr_i",
        19: "special_small_bully",
        20: "special_big_bully",
        21: "special_empty_21",
        22: "special_empty_22",
        23: "special_empty_23",
        24: "special_empty_24",
        25: "special_empty_25",
        26: "special_moving_blue_coin",
        27: "special_jrb_chest",
        28: "special_water_ring",
        29: "special_mine",
        30: "special_empty_30",
        31: "special_empty_31",
        32: "special_butterfly",
        33: "special_bowser",
        34: "special_wf_rotating_wooden_platform",
        35: "special_small_bomp",
        36: "special_wf_sliding_platform",
        37: "special_tower_platform_group",
        38: "special_rotating_counter_clockwise",
        39: "special_wf_tumbling_bridge",
        40: "special_large_bomp",

        101: "special_level_geo_03",
        102: "special_level_geo_04",
        103: "special_level_geo_05",
        104: "special_level_geo_06",
        105: "special_level_geo_07",
        106: "special_level_geo_08",
        107: "special_level_geo_09",
        108: "special_level_geo_0A",
        109: "special_level_geo_0B",
        110: "special_level_geo_0C",
        111: "special_level_geo_0D",
        112: "special_level_geo_0E",
        113: "special_level_geo_0F",
        114: "special_level_geo_10",
        115: "special_level_geo_11",
        116: "special_level_geo_12",
        117: "special_level_geo_13",
        118: "special_level_geo_14",
        119: "special_level_geo_15",
        120: "special_level_geo_16",
        121: "special_bubble_tree",
        122: "special_spiky_tree",
        123: "special_snow_tree",
        124: "special_unknown_tree",
        125: "special_palm_tree",
        126: "special_wooden_door",
        127: "special_unknown_door",
        128: "special_metal_door",
        129: "special_hmc_door",
        130: "special_unknown2_door",
        131: "special_wooden_door_warp",
        132: "special_unknown1_door_warp",
        133: "special_metal_door_warp",
        134: "special_unknown2_door_warp",
        135: "special_unknown3_door_warp",
        136: "special_castle_door_warp",
        137: "special_castle_door",
        138: "special_0stars_door",
        139: "special_1star_door",
        140: "special_3star_door",
        141: "special_key_door",

        255: "special_null_end",
    },
}

SURFACE_HAS_FORCE = [
    0x0004, # SURFACE_0004
    0x000E, # SURFACE_FLOWING_WATER
    0x002C, # SURFACE_HORIZONTAL_WIND
    0x0027, # SURFACE_MOVING_QUICKSAND
    0x0024, # SURFACE_DEEP_MOVING_QUICKSAND
    0x0025, # SURFACE_SHALLOW_MOVING_QUICKSAND
    0x002D, # SURFACE_INSTANT_MOVING_QUICKSAND
]

SPECIAL_OBJECT_PRESET_NUM_EXTRA_PARAMS = {
    0x00: 1, # SPTYPE_YROT_NO_PARAMS
    0x01: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x02: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x03: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x04: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x05: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x06: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x07: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x08: 1, # SPTYPE_YROT_NO_PARAMS
    0x09: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x0A: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x0B: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x0C: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x0D: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x0E: 1, # SPTYPE_YROT_NO_PARAMS
    0x0F: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x10: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x11: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x12: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x13: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x14: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x15: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x16: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x17: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x18: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x19: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x1A: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x1B: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x1C: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x1D: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x1E: 3, # SPTYPE_UNKNOWN,
    0x1F: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x20: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x21: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x22: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x23: 1, # SPTYPE_YROT_NO_PARAMS
    0x24: 1, # SPTYPE_YROT_NO_PARAMS
    0x25: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x26: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x27: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x28: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x65: 1, # SPTYPE_YROT_NO_PARAMS
    0x66: 1, # SPTYPE_YROT_NO_PARAMS
    0x67: 1, # SPTYPE_YROT_NO_PARAMS
    0x68: 1, # SPTYPE_YROT_NO_PARAMS
    0x69: 1, # SPTYPE_YROT_NO_PARAMS
    0x6A: 1, # SPTYPE_YROT_NO_PARAMS
    0x6B: 1, # SPTYPE_YROT_NO_PARAMS
    0x6C: 1, # SPTYPE_YROT_NO_PARAMS
    0x6D: 1, # SPTYPE_YROT_NO_PARAMS
    0x6E: 1, # SPTYPE_YROT_NO_PARAMS
    0x6F: 1, # SPTYPE_YROT_NO_PARAMS
    0x70: 1, # SPTYPE_YROT_NO_PARAMS
    0x71: 1, # SPTYPE_YROT_NO_PARAMS
    0x72: 1, # SPTYPE_YROT_NO_PARAMS
    0x73: 1, # SPTYPE_YROT_NO_PARAMS
    0x74: 1, # SPTYPE_YROT_NO_PARAMS
    0x75: 1, # SPTYPE_YROT_NO_PARAMS
    0x76: 1, # SPTYPE_YROT_NO_PARAMS
    0x77: 1, # SPTYPE_YROT_NO_PARAMS
    0x78: 1, # SPTYPE_YROT_NO_PARAMS
    0x79: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x7A: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x7B: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x7C: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x7D: 0, # SPTYPE_NO_YROT_OR_PARAMS
    0x89: 1, # SPTYPE_YROT_NO_PARAMS
    0x7E: 1, # SPTYPE_YROT_NO_PARAMS
    0x7F: 1, # SPTYPE_YROT_NO_PARAMS
    0x80: 1, # SPTYPE_YROT_NO_PARAMS
    0x81: 1, # SPTYPE_YROT_NO_PARAMS
    0x82: 1, # SPTYPE_YROT_NO_PARAMS
    0x8A: 1, # SPTYPE_DEF_PARAM_AND_YROT
    0x8B: 1, # SPTYPE_DEF_PARAM_AND_YROT
    0x8C: 1, # SPTYPE_DEF_PARAM_AND_YROT
    0x8D: 1, # SPTYPE_DEF_PARAM_AND_YROT
    0x88: 2, # SPTYPE_PARAMS_AND_YROT
    0x83: 2, # SPTYPE_PARAMS_AND_YROT
    0x84: 2, # SPTYPE_PARAMS_AND_YROT
    0x85: 2, # SPTYPE_PARAMS_AND_YROT
    0x86: 2, # SPTYPE_PARAMS_AND_YROT
    0x87: 2, # SPTYPE_PARAMS_AND_YROT
    0xFF: 0, # SPTYPE_NO_YROT_OR_PARAMS
}

SPECIAL_OBJECT_PRESET_COMMANDS = {
    0: "SPECIAL_OBJECT",
    1: "SPECIAL_OBJECT_WITH_YAW",
    2: "SPECIAL_OBJECT_WITH_YAW_AND_PARAM",
    3: "SPECIAL_OBJECT_UNKNOWN", # unused
}


def collision_command_arg_to_str(name: str, value: int, argtype: str) -> str:
    if name in COLLISION_CONSTANTS and value in COLLISION_CONSTANTS[name]:
        return COLLISION_CONSTANTS[name][value]
    return value_to_str(value, 0, 16, argtype)


def collision_command_to_str(command: str, *args) -> str:
    return "    %s(%s),\n" % (
        command,
        ", ".join([
            collision_command_arg_to_str(arg["name"], arg["value"], arg["argtype"])
            for arg in args
        ])
    )


#
# Collision commands
#


def process_col_init(buffer: list, index: int) -> tuple[str, int]:
    cmd = collision_command_to_str("COL_INIT")
    res, index = process_col_vertex_init(buffer, index + 1)
    return cmd + res, index


def process_col_vertex_init(buffer: list, index: int) -> tuple[str, int]:
    num_verts = buffer[index]
    cmd = collision_command_to_str("COL_VERTEX_INIT",
        { "name": "vtxNum", "value": num_verts, "argtype": "u" },
    )
    index += 1
    for _ in range(num_verts):
        res, index = process_col_vertex(buffer, index)
        cmd += res
    return cmd, index


def process_col_vertex(buffer: list, index: int) -> tuple[str, int]:
    x, y, z = buffer[index:index+3]
    cmd = collision_command_to_str("COL_VERTEX",
        { "name": "x", "value": x, "argtype": "s" },
        { "name": "y", "value": y, "argtype": "s" },
        { "name": "z", "value": z, "argtype": "s" },
    )
    return cmd, index + 3


def process_col_tri_init(buffer: list, index: int) -> tuple[str, int]:
    surf_type, num_tris = buffer[index:index+2]
    cmd = collision_command_to_str("COL_TRI_INIT",
        { "name": "surfType", "value": surf_type, "argtype": "x" },
        { "name": "triNum", "value": num_tris, "argtype": "u" },
    )
    index += 2
    process_col_tri_func = process_col_tri_special if surf_type in SURFACE_HAS_FORCE else process_col_tri
    for _ in range(num_tris):
        res, index = process_col_tri_func(buffer, index)
        cmd += res
    return cmd, index


def process_col_tri(buffer: list, index: int) -> tuple[str, int]:
    v1, v2, v3 = buffer[index:index+3]
    cmd = collision_command_to_str("COL_TRI",
        { "name": "v1", "value": v1, "argtype": "u" },
        { "name": "v2", "value": v2, "argtype": "u" },
        { "name": "v3", "value": v3, "argtype": "u" },
    )
    return cmd, index + 3


def process_col_tri_special(buffer: list, index: int) -> tuple[str, int]:
    v1, v2, v3, param = buffer[index:index+4]
    cmd = collision_command_to_str("COL_TRI_SPECIAL",
        { "name": "v1", "value": v1, "argtype": "u" },
        { "name": "v2", "value": v2, "argtype": "u" },
        { "name": "v3", "value": v3, "argtype": "u" },
        { "name": "param", "value": param, "argtype": "x" },
    )
    return cmd, index + 3


def process_col_tri_stop(buffer: list, index: int) -> tuple[str, int]:
    cmd = collision_command_to_str("COL_TRI_STOP")
    return cmd, index + 1


def process_col_end(buffer: list, index: int) -> tuple[str, int]:
    cmd = collision_command_to_str("COL_END")
    return cmd, -1


def process_col_special_init(buffer: list, index: int) -> tuple[str, int]:
    num_objs = buffer[index + 1]
    cmd = collision_command_to_str("COL_SPECIAL_INIT",
        { "name": "num", "value": num_objs, "argtype": "u" },
    )
    index += 2
    for _ in range(num_objs):
        res, index = process_special_object(buffer, index)
        cmd += res
    return cmd, index


def process_col_water_box_init(buffer: list, index: int) -> tuple[str, int]:
    num_boxes = buffer[index + 1]
    cmd = collision_command_to_str("COL_WATER_BOX_INIT",
        { "name": "num", "value": num_boxes, "argtype": "u" },
    )
    index += 2
    for _ in range(num_boxes):
        res, index = process_col_water_box(buffer, index)
        cmd += res
    return cmd, index


def process_col_water_box(buffer: list, index: int) -> tuple[str, int]:
    id, x1, z1, x2, z2, y = buffer[index:index+7]
    cmd = collision_command_to_str("COL_WATER_BOX_INIT",
        { "name": "id", "value": id, "argtype": "u" },
        { "name": "x1", "value": x1, "argtype": "s" },
        { "name": "z1", "value": z1, "argtype": "s" },
        { "name": "x2", "value": x2, "argtype": "s" },
        { "name": "z2", "value": z2, "argtype": "s" },
        { "name": "y", "value": y, "argtype": "s" },
    )
    return cmd, index + 6


def process_special_object(buffer: list, index: int) -> tuple[str, int]:
    preset, posX, posY, posZ = buffer[index:index+5]
    extra_params = SPECIAL_OBJECT_PRESET_NUM_EXTRA_PARAMS[preset]
    cmd = collision_command_to_str(SPECIAL_OBJECT_PRESET_COMMANDS[extra_params],
        { "name": "preset", "value": preset, "argtype": "u" },
        { "name": "posX", "value": posX, "argtype": "s" },
        { "name": "posY", "value": posY, "argtype": "s" },
        { "name": "posZ", "value": posZ, "argtype": "s" },
        *[
            { "name": "extra_%d" % i, "value": buffer[4 + i], "argtype": "s" }
            for i in range(extra_params)
        ]
    )
    return cmd, index + 4 + extra_params


COLLISION_COMMANDS = {
    0x0040: process_col_init,           # TERRAIN_LOAD_VERTICES
    0x0041: process_col_tri_stop,       # TERRAIN_LOAD_CONTINUE
    0x0042: process_col_end,            # TERRAIN_LOAD_END
    0x0043: process_col_special_init,   # TERRAIN_LOAD_OBJECTS
    0x0044: process_col_water_box_init, # TERRAIN_LOAD_ENVIRONMENT
    **{
        surf_type: process_col_tri_init
        for surf_type in COLLISION_CONSTANTS["surfType"]
    }
}


@GfxData.writer()
def write_collision_inc_c(self: GfxData, dirpath: str):
    with open(os.path.join(dirpath, "collision.inc.c"), "w", newline="\n") as collision_inc_c:
        for name, collision in self.collisions.items():
            collision_inc_c.write("Collision %s[] = {\n" % (name))
            index = 0
            buffer = collision.buffer
            while index < len(buffer):
                cmd = buffer[index]

                if cmd not in COLLISION_COMMANDS:
                    prints.warning("Unknown collision command: 0x%04X\nAborting collision parsing; Collision may be incomplete" % (cmd, name))
                    break

                collision_str, index = COLLISION_COMMANDS[cmd](buffer, index)
                collision_inc_c.write(collision_str)
                if index == -1: # COL_END
                    break

            else: # Missing COL_END, add it silently
                collision_str, index = process_col_end(buffer, 0)
                collision_inc_c.write(collision_str)

            collision_inc_c.write("};\n\n")
