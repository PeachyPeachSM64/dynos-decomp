import os
from .. import prints
from ..consts.bhv import BEHAVIOR_IDS
from ..consts.objects import OBJECT_FIELDS
from ..gfxdata import GfxData


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
        str(i): name
        for i, name in enumerate(BEHAVIOR_IDS)
    },
    "field": {
        str(i): name
        for i, name in enumerate(OBJECT_FIELDS)
    }
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


def define_behavior_command(name: str, argnames: str, *commands):
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
        "args": args
    }


BEHAVIOR_COMMANDS = [

define_behavior_command(
    "BEGIN",
    "objList",
        BC_BB(0x00, "objList")
),





define_behavior_command(
    "ID",
    "id",
        BC_B0H(0x39, "id")
),





]




# @GfxData.writer()
# def write_behavior_data_c(behavior_data_filepath: str, gfxdata: GfxData):
#     with open(behavior_data_filepath, "w", newline="\n") as behavior_data_c:
#         for name, behavior in gfxdata.behaviors.items():
#             behavior_data_c.write("const BehaviorScript %s[] = {\n" % (name))

#             behavior_data_c.write("};\n\n")


# const BehaviorScript bhv1Up[] = {
#     BEGIN(OBJ_LIST_LEVEL),
#     ID(id_bhv1Up),
#     OR_INT(oFlags, OBJ_FLAG_UPDATE_GFX_POS_AND_ANGLE),
#     BILLBOARD(),
#     SET_HITBOX_WITH_OFFSET(/*Radius*/ 30, /*Height*/ 30, /*Downwards offset*/ 0),
#     SET_FLOAT(oGraphYOffset, 30),
#     CALL_NATIVE(bhv_1up_init),
#     BEGIN_LOOP(),
#         SET_INT(oIntangibleTimer, 0),
#         CALL_NATIVE(bhv_1up_loop),
#     END_LOOP(),
# };

