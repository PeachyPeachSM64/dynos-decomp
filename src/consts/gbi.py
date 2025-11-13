def C(w: int, pos: int, width: int) -> int: return ((w >> pos) & ((1 << width) - 1))

#
# RSP commands
#

G_NOOP = 0x00
G_SETOTHERMODE_H = 0xe3
G_SETOTHERMODE_L = 0xe2
G_SPNOOP = 0xe0
G_ENDDL = 0xdf
G_DL = 0xde
G_MOVEMEM = 0xdc
G_MOVEWORD = 0xdb
G_MTX = 0xda
G_GEOMETRYMODE = 0xd9
G_POPMTX = 0xd8
G_TEXTURE = 0xd7
G_COPYMEM = 0xd2
G_VTX = 0x01
G_TRI1 = 0x05
G_TRI2 = 0x06

#
# RDP commands
#

G_SETCIMG = 0xff
G_SETZIMG = 0xfe
G_SETTIMG = 0xfd
G_SETCOMBINE = 0xfc
G_SETENVCOLOR = 0xfb
G_SETPRIMCOLOR = 0xfa
G_SETBLENDCOLOR = 0xf9
G_SETFOGCOLOR = 0xf8
G_SETFILLCOLOR = 0xf7
G_FILLRECT = 0xf6
G_SETTILE = 0xf5
G_LOADTILE = 0xf4
G_LOADBLOCK = 0xf3
G_SETTILESIZE = 0xf2
G_LOADTLUT = 0xf0
G_SETSCISSOR = 0xed
G_RDPFULLSYNC = 0xe9
G_RDPTILESYNC = 0xe8
G_RDPPIPESYNC = 0xe7
G_RDPLOADSYNC = 0xe6
G_TEXRECTFLIP = 0xe5
G_TEXRECT = 0xe4

#
# Extended commands
#

G_VTX_EXT = 0x11
G_TRI2_EXT = 0x12
G_PPARTTOCOLOR = 0xd3
G_SETENVRGB = 0xd1

#
# G_SETOTHERMODE_H
#

G_MDSFT_ALPHADITHER = 4
G_MDSFT_RGBDITHER = 6
G_MDSFT_COMBKEY = 8
G_MDSFT_TEXTCONV = 9
G_MDSFT_TEXTFILT = 12
G_MDSFT_TEXTLUT = 14
G_MDSFT_TEXTLOD = 16
G_MDSFT_TEXTDETAIL = 17
G_MDSFT_TEXTPERSP = 19
G_MDSFT_CYCLETYPE = 20
G_MDSFT_PIPELINE = 23

G_SETOTHERMODE_H_SHIFTS = {
    G_MDSFT_ALPHADITHER: {
        "cmd": "gsDPSetAlphaDither",
        "consts": {
            (0 << G_MDSFT_ALPHADITHER): "G_AD_PATTERN",
            (1 << G_MDSFT_ALPHADITHER): "G_AD_NOTPATTERN",
            (2 << G_MDSFT_ALPHADITHER): "G_AD_NOISE",
            (3 << G_MDSFT_ALPHADITHER): "G_AD_DISABLE",
        },
    },
    G_MDSFT_RGBDITHER: {
        "cmd": "gsDPSetColorDither",
        "consts": {
            (0 << G_MDSFT_RGBDITHER): "G_CD_MAGICSQ",
            (1 << G_MDSFT_RGBDITHER): "G_CD_BAYER",
            (2 << G_MDSFT_RGBDITHER): "G_CD_NOISE",
            (3 << G_MDSFT_RGBDITHER): "G_CD_DISABLE",
        },
    },
    G_MDSFT_COMBKEY: {
        "cmd": "gsDPSetCombineKey",
        "consts": {
            (0 << G_MDSFT_COMBKEY): "G_CK_NONE",
            (1 << G_MDSFT_COMBKEY): "G_CK_KEY",
        },
    },
    G_MDSFT_TEXTCONV: {
        "cmd": "gsDPSetTextureConvert",
        "consts": {
            (0 << G_MDSFT_TEXTCONV): "G_TC_CONV",
            (5 << G_MDSFT_TEXTCONV): "G_TC_FILTCONV",
            (6 << G_MDSFT_TEXTCONV): "G_TC_FILT",
        },
    },
    G_MDSFT_TEXTFILT: {
        "cmd": "gsDPSetTextureFilter",
        "consts": {
            (0 << G_MDSFT_TEXTFILT): "G_TF_POINT",
            (3 << G_MDSFT_TEXTFILT): "G_TF_AVERAGE",
            (2 << G_MDSFT_TEXTFILT): "G_TF_BILERP",
        },
    },
    G_MDSFT_TEXTLUT: {
        "cmd": "gsDPSetTextureLUT",
        "consts": {
            (0 << G_MDSFT_TEXTLUT): "G_TT_NONE",
            (2 << G_MDSFT_TEXTLUT): "G_TT_RGBA16",
            (3 << G_MDSFT_TEXTLUT): "G_TT_IA16",
        },
    },
    G_MDSFT_TEXTLOD: {
        "cmd": "gsDPSetTextureLOD",
        "consts": {
            (0 << G_MDSFT_TEXTLOD): "G_TL_TILE",
            (1 << G_MDSFT_TEXTLOD): "G_TL_LOD",
        },
    },
    G_MDSFT_TEXTDETAIL: {
        "cmd": "gsDPSetTextureDetail",
        "consts": {
            (0 << G_MDSFT_TEXTDETAIL): "G_TD_CLAMP",
            (1 << G_MDSFT_TEXTDETAIL): "G_TD_SHARPEN",
            (2 << G_MDSFT_TEXTDETAIL): "G_TD_DETAIL",
        },
    },
    G_MDSFT_TEXTPERSP: {
        "cmd": "gsDPSetTexturePersp",
        "consts": {
            (0 << G_MDSFT_TEXTPERSP): "G_TP_NONE",
            (1 << G_MDSFT_TEXTPERSP): "G_TP_PERSP",
        },
    },
    G_MDSFT_CYCLETYPE: {
        "cmd": "gsDPSetCycleType",
        "consts": {
            (0 << G_MDSFT_CYCLETYPE): "G_CYC_1CYCLE",
            (1 << G_MDSFT_CYCLETYPE): "G_CYC_2CYCLE",
            (2 << G_MDSFT_CYCLETYPE): "G_CYC_COPY",
            (3 << G_MDSFT_CYCLETYPE): "G_CYC_FILL",
        },
    },
    G_MDSFT_PIPELINE: {
        "cmd": "gsDPPipelineMode",
        "consts": {
            (0 << G_MDSFT_PIPELINE): "G_PM_NPRIMITIVE",
            (1 << G_MDSFT_PIPELINE): "G_PM_1PRIMITIVE",
        },
    },
}

#
# G_SETOTHERMODE_L
#

G_MDSFT_ALPHACOMPARE = 0
G_MDSFT_ZSRCSEL = 2
# G_MDSFT_RENDERMODE = 3 --- This thing has too much macros

G_SETOTHERMODE_L_SHIFTS = {
    G_MDSFT_ALPHACOMPARE: {
        "cmd": "gsDPSetAlphaCompare",
        "consts": {
            (0 << G_MDSFT_ALPHACOMPARE): "G_AC_NONE",
            (1 << G_MDSFT_ALPHACOMPARE): "G_AC_THRESHOLD",
            (3 << G_MDSFT_ALPHACOMPARE): "G_AC_DITHER",
        },
    },
    G_MDSFT_ZSRCSEL: {
        "cmd": "gsDPSetDepthSource",
        "consts": {
            (0 << G_MDSFT_ZSRCSEL): "G_ZS_PIXEL",
            (1 << G_MDSFT_ZSRCSEL): "G_ZS_PRIM",
        },
    },
    # G_MDSFT_RENDERMODE: {
    #     "cmd": "gsDPSetRenderMode",
    #     "consts": {},
    # },
}

#
# G_MOVEMEM
#

G_MV_VIEWPORT = 8
G_MV_LIGHT = 10

#
# G_MOVEWORD
#

G_MW_NUMLIGHT = 0x02
G_MW_FOG = 0x08
G_MW_FX = 0x00
G_MW_LIGHTCOL = 0x0A

G_MWO_FRESNEL = 0x0C

G_MOVEWORD_LIGHTS = {
    1: "LIGHT_1",
    2: "LIGHT_2",
    3: "LIGHT_3",
    4: "LIGHT_4",
    5: "LIGHT_5",
    6: "LIGHT_6",
    7: "LIGHT_7",
    8: "LIGHT_8",
}

#
# G_MTX
#

G_MTX_PROJECTION = 0x04
G_MTX_LOAD = 0x02
G_MTX_PUSH = 0x01

G_MTX_FLAGS = {
    G_MTX_PROJECTION: "G_MTX_PROJECTION",
    G_MTX_LOAD: "G_MTX_LOAD",
    G_MTX_PUSH: "G_MTX_PUSH",
}

#
# G_GEOMETRYMODE
#

G_GEOMETRYMODE_FLAGS = {
    0x000001: "G_ZBUFFER",
  # 0x000002: "<unused>",
    0x000004: "G_SHADE",
  # 0x000008: "<unused>",
  # 0x000010: "<unused>",
  # 0x000020: "<unused>",
    0x000040: "G_FRESNEL_COLOR_EXT",
    0x000080: "G_PACKED_NORMALS_EXT",
  # 0x000100: "<unused>",
    0x000200: "G_CULL_FRONT",
    0x000400: "G_CULL_BACK",
    0x000800: "G_LIGHT_MAP_EXT",
  # 0x001000: "<unused>",
  # 0x002000: "<unused>",
    0x004000: "G_LIGHTING_ENGINE_EXT",
  # 0x008000: "<unused>",
    0x010000: "G_FOG",
    0x020000: "G_LIGHTING",
    0x040000: "G_TEXTURE_GEN",
    0x080000: "G_TEXTURE_GEN_LINEAR",
    0x100000: "G_LOD",
    0x200000: "G_SHADING_SMOOTH",
    0x400000: "G_FRESNEL_ALPHA_EXT",
    0x800000: "G_CLIPPING",
}

#
# G_TEXTURE
#

G_ON_OFF = {
    0: "G_OFF",
    1: "G_ON",
}

G_TEXTURE_TILES = {
    7: "G_TX_LOADTILE",
    0: "G_TX_RENDERTILE",
}

#
# G_COPYMEM
#

G_COPYMEM_BODY_PARTS = {
    0: "PANTS",
    1: "SHIRT",
    2: "GLOVES",
    3: "SHOES",
    4: "HAIR",
    5: "SKIN",
    6: "CAP",
    7: "EMBLEM",
}

#
# G_SETIMG
#

G_SETIMG_FMT = {
    0: "G_IM_FMT_RGBA",
    1: "G_IM_FMT_YUV",
    2: "G_IM_FMT_CI",
    3: "G_IM_FMT_IA",
    4: "G_IM_FMT_I",
}

G_SETIMG_SIZ = {
    0: "G_IM_SIZ_4b",
    1: "G_IM_SIZ_8b",
    2: "G_IM_SIZ_16b",
    3: "G_IM_SIZ_32b",
    5: "G_IM_SIZ_DD",
}

#
# G_SETTILE
#

G_SETTILE_FMT = G_SETIMG_FMT
G_SETTILE_SIZ = G_SETIMG_SIZ
G_SETTILE_TILES = G_TEXTURE_TILES

G_SETTILE_FLAGS = {
    0x1: "G_TX_MIRROR",
    0x2: "G_TX_CLAMP",
}

#
# G_LOADTILE
#

G_LOADTILE_TILES = G_TEXTURE_TILES

#
# G_LOADBLOCK
#

G_LOADBLOCK_TILES = G_TEXTURE_TILES

#
# G_SETTILESIZE
#

G_SETTILESIZE_TILES = G_TEXTURE_TILES

#
# G_LOADTLUT
#

G_LOADTLUT_TILES = G_TEXTURE_TILES

#
# G_SETSCISSOR
#

G_SETSCISSOR_MODES = {
    0: "G_SC_NON_INTERLACE",
    3: "G_SC_ODD_INTERLACE",
    2: "G_SC_EVEN_INTERLACE",
}

#
# G_SETCOMBINE
#

# https://wiki.cloudmodding.com/oot/F3DZEX2#Color_Combiner_Settings
G_SETCOMBINE_COLOR_COMBINERS = {
    "a": {
        0x0: "COMBINED",
        0x1: "TEXEL0",
        0x2: "TEXEL1",
        0x3: "PRIMITIVE",
        0x4: "SHADE",
        0x5: "ENVIRONMENT",
        0x6: "1",
        0x7: "NOISE",
    },
    "b": {
        0x0: "COMBINED",
        0x1: "TEXEL0",
        0x2: "TEXEL1",
        0x3: "PRIMITIVE",
        0x4: "SHADE",
        0x5: "ENVIRONMENT",
        0x6: "CENTER",
        0x7: "K4",
    },
    "c": {
        0x0: "COMBINED",
        0x1: "TEXEL0",
        0x2: "TEXEL1",
        0x3: "PRIMITIVE",
        0x4: "SHADE",
        0x5: "ENVIRONMENT",
        0x6: "SCALE",
        0x7: "COMBINED_ALPHA",
        0x8: "TEXEL0_ALPHA",
        0x9: "TEXEL1_ALPHA",
        0xA: "PRIMITIVE_ALPHA",
        0xB: "SHADE_ALPHA",
        0xC: "ENV_ALPHA",
        0xD: "LOD_FRACTION",
        0xE: "PRIM_LOD_FRAC",
        0xF: "K5",
    },
    "d": {
        0x0: "COMBINED",
        0x1: "TEXEL0",
        0x2: "TEXEL1",
        0x3: "PRIMITIVE",
        0x4: "SHADE",
        0x5: "ENVIRONMENT",
        0x6: "1",
    },
}

G_SETCOMBINE_ALPHA_COMBINERS = {
    "a": {
        0x0: "COMBINED",
        0x1: "TEXEL0",
        0x2: "TEXEL1",
        0x3: "PRIMITIVE",
        0x4: "SHADE",
        0x5: "ENVIRONMENT",
        0x6: "1",
    },
    "b": {
        0x0: "COMBINED",
        0x1: "TEXEL0",
        0x2: "TEXEL1",
        0x3: "PRIMITIVE",
        0x4: "SHADE",
        0x5: "ENVIRONMENT",
        0x6: "1",
    },
    "c": {
        0x0: "LOD_FRACTION",
        0x1: "TEXEL0",
        0x2: "TEXEL1",
        0x3: "PRIMITIVE",
        0x4: "SHADE",
        0x5: "ENVIRONMENT",
        0x6: "PRIM_LOD_FRAC",
    },
    "d": {
        0x0: "COMBINED",
        0x1: "TEXEL0",
        0x2: "TEXEL1",
        0x3: "PRIMITIVE",
        0x4: "SHADE",
        0x5: "ENVIRONMENT",
        0x6: "1",
    },
}

G_SETCOMBINE_MODES = {
    "0, 0, 0, PRIMITIVE, 0, 0, 0, PRIMITIVE":
        "G_CC_PRIMITIVE",
    "0, 0, 0, SHADE, 0, 0, 0, SHADE":
        "G_CC_SHADE",
    "TEXEL0, 0, SHADE, 0, 0, 0, 0, SHADE":
        "G_CC_MODULATEI",
    "TEXEL0, 0, SHADE, 0, 0, 0, 0, TEXEL0":
        "G_CC_MODULATEIDECALA",
    "TEXEL0, 0, SHADE, 0, 0, 0, 0, ENVIRONMENT":
        "G_CC_MODULATEIFADE",
    "G_CC_MODULATEI":
        "G_CC_MODULATERGB",
    "G_CC_MODULATEIDECALA":
        "G_CC_MODULATERGBDECALA",
    "G_CC_MODULATEIFADE":
        "G_CC_MODULATERGBFADE",
    "TEXEL0, 0, SHADE, 0, TEXEL0, 0, SHADE, 0":
        "G_CC_MODULATEIA",
    "TEXEL0, 0, SHADE, 0, TEXEL0, 0, ENVIRONMENT, 0":
        "G_CC_MODULATEIFADEA",
    "TEXEL0, 0, SHADE, 0, ENVIRONMENT, 0, TEXEL0, 0":
        "G_CC_MODULATEFADE",
    "G_CC_MODULATEIA":
        "G_CC_MODULATERGBA",
    "G_CC_MODULATEIFADEA":
        "G_CC_MODULATERGBFADEA",
    "TEXEL0, 0, PRIMITIVE, 0, 0, 0, 0, PRIMITIVE":
        "G_CC_MODULATEI_PRIM",
    "TEXEL0, 0, PRIMITIVE, 0, TEXEL0, 0, PRIMITIVE, 0":
        "G_CC_MODULATEIA_PRIM",
    "TEXEL0, 0, PRIMITIVE, 0, 0, 0, 0, TEXEL0":
        "G_CC_MODULATEIDECALA_PRIM",
    "G_CC_MODULATEI_PRIM":
        "G_CC_MODULATERGB_PRIM",
    "G_CC_MODULATEIA_PRIM":
        "G_CC_MODULATERGBA_PRIM",
    "G_CC_MODULATEIDECALA_PRIM":
        "G_CC_MODULATERGBDECALA_PRIM",
    "SHADE, 0, ENVIRONMENT, 0, SHADE, 0, ENVIRONMENT, 0":
        "G_CC_FADE",
    "TEXEL0, 0, ENVIRONMENT, 0, TEXEL0, 0, ENVIRONMENT, 0":
        "G_CC_FADEA",
    "0, 0, 0, TEXEL0, 0, 0, 0, SHADE":
        "G_CC_DECALRGB",
    "0, 0, 0, TEXEL0, 0, 0, 0, TEXEL0":
        "G_CC_DECALRGBA",
    "0, 0, 0, TEXEL0, 0, 0, 0, ENVIRONMENT":
        "G_CC_DECALFADE",
    "0, 0, 0, TEXEL0, TEXEL0, 0, ENVIRONMENT, 0":
        "G_CC_DECALFADEA",
    "ENVIRONMENT, SHADE, TEXEL0, SHADE, 0, 0, 0, SHADE":
        "G_CC_BLENDI",
    "ENVIRONMENT, SHADE, TEXEL0, SHADE, TEXEL0, 0, SHADE, 0":
        "G_CC_BLENDIA",
    "ENVIRONMENT, SHADE, TEXEL0, SHADE, 0, 0, 0, TEXEL0":
        "G_CC_BLENDIDECALA",
    "TEXEL0, SHADE, TEXEL0_ALPHA, SHADE, 0, 0, 0, SHADE":
        "G_CC_BLENDRGBA",
    "TEXEL0, SHADE, TEXEL0_ALPHA, SHADE, 0, 0, 0, TEXEL0":
        "G_CC_BLENDRGBDECALA",
    "TEXEL0, SHADE, TEXEL0_ALPHA, SHADE, 0, 0, 0, ENVIRONMENT":
        "G_CC_BLENDRGBFADEA",
    "TEXEL0, 0, TEXEL0, SHADE, 0, 0, 0, SHADE":
        "G_CC_ADDRGB",
    "TEXEL0, 0, TEXEL0, SHADE, 0, 0, 0, TEXEL0":
        "G_CC_ADDRGBDECALA",
    "TEXEL0, 0, TEXEL0, SHADE, 0, 0, 0, ENVIRONMENT":
        "G_CC_ADDRGBFADE",
    "ENVIRONMENT, 0, TEXEL0, SHADE, 0, 0, 0, SHADE":
        "G_CC_REFLECTRGB",
    "ENVIRONMENT, 0, TEXEL0, SHADE, 0, 0, 0, TEXEL0":
        "G_CC_REFLECTRGBDECALA",
    "PRIMITIVE, SHADE, TEXEL0, SHADE, 0, 0, 0, SHADE":
        "G_CC_HILITERGB",
    "PRIMITIVE, SHADE, TEXEL0, SHADE, PRIMITIVE, SHADE, TEXEL0, SHADE":
        "G_CC_HILITERGBA",
    "PRIMITIVE, SHADE, TEXEL0, SHADE, 0, 0, 0, TEXEL0":
        "G_CC_HILITERGBDECALA",
    "0, 0, 0, SHADE, 0, 0, 0, TEXEL0":
        "G_CC_SHADEDECALA",
    "0, 0, 0, SHADE, 0, 0, 0, ENVIRONMENT":
        "G_CC_SHADEFADEA",
    "PRIMITIVE, ENVIRONMENT, TEXEL0, ENVIRONMENT, TEXEL0, 0, SHADE, 0":
        "G_CC_BLENDPE",
    "PRIMITIVE, ENVIRONMENT, TEXEL0, ENVIRONMENT, 0, 0, 0, TEXEL0":
        "G_CC_BLENDPEDECALA",
    "ENVIRONMENT, PRIMITIVE, TEXEL0, PRIMITIVE, TEXEL0, 0, SHADE, 0":
        "_G_CC_BLENDPE",
    "ENVIRONMENT, PRIMITIVE, TEXEL0, PRIMITIVE, 0, 0, 0, TEXEL0":
        "_G_CC_BLENDPEDECALA",
    "PRIMITIVE, SHADE, TEXEL0, SHADE, 0, 0, 0, SHADE":
        "_G_CC_TWOCOLORTEX",
    "PRIMITIVE, TEXEL0, LOD_FRACTION, TEXEL0, PRIMITIVE, TEXEL0, LOD_FRACTION, TEXEL0":
        "_G_CC_SPARSEST",
    "TEXEL1, TEXEL0, PRIM_LOD_FRAC, TEXEL0, TEXEL1, TEXEL0, PRIM_LOD_FRAC, TEXEL0":
        "G_CC_TEMPLERP",
    "TEXEL1, TEXEL0, LOD_FRACTION, TEXEL0, TEXEL1, TEXEL0, LOD_FRACTION, TEXEL0":
        "G_CC_TRILERP",
    "TEXEL0, 0, TEXEL1, 0, TEXEL0, 0, TEXEL1, 0":
        "G_CC_INTERFERENCE",
    "TEXEL0, K4, K5, TEXEL0, 0, 0, 0, SHADE":
        "G_CC_1CYUV2RGB",
    "TEXEL1, K4, K5, TEXEL1, 0, 0, 0, 0":
        "G_CC_YUV2RGB",
    "0, 0, 0, COMBINED, 0, 0, 0, COMBINED":
        "G_CC_PASS2",
    "COMBINED, 0, SHADE, 0, 0, 0, 0, SHADE":
        "G_CC_MODULATEI2",
    "COMBINED, 0, SHADE, 0, COMBINED, 0, SHADE, 0":
        "G_CC_MODULATEIA2",
    "G_CC_MODULATEI2":
        "G_CC_MODULATERGB2",
    "G_CC_MODULATEIA2":
        "G_CC_MODULATERGBA2",
    "COMBINED, 0, PRIMITIVE, 0, 0, 0, 0, PRIMITIVE":
        "G_CC_MODULATEI_PRIM2",
    "COMBINED, 0, PRIMITIVE, 0, COMBINED, 0, PRIMITIVE, 0":
        "G_CC_MODULATEIA_PRIM2",
    "G_CC_MODULATEI_PRIM2":
        "G_CC_MODULATERGB_PRIM2",
    "G_CC_MODULATEIA_PRIM2":
        "G_CC_MODULATERGBA_PRIM2",
    "0, 0, 0, COMBINED, 0, 0, 0, SHADE":
        "G_CC_DECALRGB2",
    "COMBINED, SHADE, COMBINED_ALPHA, SHADE, 0, 0, 0, SHADE":
        "G_CC_DECALRGBA2",
    "ENVIRONMENT, SHADE, COMBINED, SHADE, 0, 0, 0, SHADE":
        "G_CC_BLENDI2",
    "ENVIRONMENT, SHADE, COMBINED, SHADE, COMBINED, 0, SHADE, 0":
        "G_CC_BLENDIA2",
    "TEXEL0, CENTER, SCALE, 0, 0, 0, 0, 0":
        "G_CC_CHROMA_KEY2",
    "ENVIRONMENT, COMBINED, TEXEL0, COMBINED, 0, 0, 0, SHADE":
        "G_CC_HILITERGB2",
    "ENVIRONMENT, COMBINED, TEXEL0, COMBINED, ENVIRONMENT, COMBINED, TEXEL0, COMBINED":
        "G_CC_HILITERGBA2",
    "ENVIRONMENT, COMBINED, TEXEL0, COMBINED, 0, 0, 0, TEXEL0":
        "G_CC_HILITERGBDECALA2",
    "ENVIRONMENT, COMBINED, TEXEL0, COMBINED, 0, 0, 0, COMBINED":
        "G_CC_HILITERGBPASSA2",
}

#
# G_PPARTTOCOLOR
#

G_PPARTTOCOLOR_COLORS = {
    0x0: "G_COL_PRIM",
    0x1: "G_COL_ENV",
}

G_PPARTTOCOLOR_OFFSETS = {
    0x0: "G_CP_LIGHT",
    0x1: "G_CP_AMBIENT",
}

G_PPARTTOCOLOR_BODY_PARTS = G_COPYMEM_BODY_PARTS
