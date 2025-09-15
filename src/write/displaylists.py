import os
from .. import prints
from ..consts.gbi import *
from ..gfxdata import GfxData
from .values import get_pointer_and_offset, get_named_flags, bnot


class GfxCtx:
    def __init__(self, buffer: list, gfxdata: GfxData):
        self.buffer = buffer
        self.gfxdata = gfxdata

    def w(self, offset: int, index: int):
        return self.buffer[2 * offset + index]

    @property
    def w0(self):
        return self.w(0, 0)

    @property
    def w1(self):
        return self.w(0, 1)


#
# RSP commands
#

def g_noop(ctx: GfxCtx):
    tag = ctx.w1
    if tag == 0:
        return "gsDPNoOp()", 0
    return f"gsDPNoOpTag(0x{tag:X})", 0

def g_setothermode(ctx: GfxCtx, op, shifts):
    c88 = C(ctx.w0, 8, 8)
    c08 = C(ctx.w0, 0, 8)
    length = c08 + 1
    shift = 32 - c88 - length
    mode = ctx.w1
    cmd = shifts.get(shift)
    if cmd is not None:
        const = cmd["consts"].get(mode, f"0x{mode:X}")
        return f"{cmd['cmd']}({const})", 0
    return f"gsSPSetOtherMode({op}, {shift}, {length}, 0x{mode:X})", 0

def g_spnoop(ctx: GfxCtx):
    return "gsSPNoOp()", 0

def g_enddl(ctx: GfxCtx):
    return "gsSPEndDisplayList()", 0

def g_dl(ctx: GfxCtx):
    branch = C(ctx.w0, 16, 8)
    dl, _ = get_pointer_and_offset(ctx.w1)
    if branch == 1:
        return f"gsSPBranchList({dl})", 0
    return f"gsSPDisplayList({dl})", 0

def g_movemem(ctx: GfxCtx):
    idx = C(ctx.w0, 0, 8)
    if idx == G_MV_VIEWPORT:
        return f"gsSPViewport({ctx.w1})", 0
    if idx == G_MV_LIGHT:
        light, offset = get_pointer_and_offset(ctx.w1)
        lightidx = (C(ctx.w0, 8, 8) * 8) // 24 - 1
        if light in ctx.gfxdata.lights1:
            return f"gsSPLight(&{light}.{'l' if offset == 1 else 'a'}, {lightidx})", 0
        return f"gsSPLight({light}, {lightidx})", 0
    adrs = ctx.w1
    length = C(ctx.w0, 19, 5) * 8 + 1
    ofs = C(ctx.w0, 8, 8) * 8
    return f"gsDma2p(G_MOVEMEM, {adrs}, {length}, {idx}, {ofs})", 0

def g_moveword(ctx: GfxCtx):
    idx = C(ctx.w0, 16, 8)
    offset = C(ctx.w0, 0, 16)
    if idx == G_MW_NUMLIGHT:
        num_lights = ctx.w1 // 24
        light, _ = get_pointer_and_offset(ctx.w(1, 1))
        return f"gsSPSetLights{num_lights}({light})", num_lights + 1
    elif idx == G_MW_FOG:
        fm = C(ctx.w1, 16, 16)
        fo = C(ctx.w1, 0, 16)
        return f"gsSPFogFactor(0x{fm:X}, 0x{fo:X})", 0
    elif idx == G_MW_FX and offset == G_MWO_FRESNEL:
        fs = C(ctx.w1, 16, 16)
        fo = C(ctx.w1, 0, 16)
        return f"gsSPFresnel(0x{fs:X}, 0x{fo:X})", 0
    elif idx == G_MW_LIGHTCOL:
        light = (offset // 24) + 1
        light_str = G_MOVEWORD_LIGHTS.get(light, f"{light}")
        return f"gsSPLightColor({light_str}, 0x{ctx.w1:08X})", 1
    data = ctx.w1
    return f"gsMoveWd({idx}, {offset}, {data})", 0

def g_mtx(ctx: GfxCtx):
    flags = C(ctx.w0, 0, 8) ^ G_MTX_PUSH
    params = get_named_flags(flags, G_MTX_FLAGS)
    mtx = ctx.w1
    return f"gsSPMatrix({mtx}, {params})", 0

def g_geometrymode(ctx: GfxCtx):
    set_flags = ctx.w1 & 0xFFFFFF
    set_params = get_named_flags(set_flags, G_GEOMETRYMODE_FLAGS)
    clr_flags = bnot(C(ctx.w0, 0, 24), 24) & 0xFFFFFF
    clr_params = get_named_flags(clr_flags, G_GEOMETRYMODE_FLAGS)
    if clr_flags == 0xFFFFFF:
        return f"gsSPLoadGeometryMode({set_params})", 0
    if set_flags == 0:
        return f"gsSPClearGeometryMode({clr_params})", 0
    if clr_flags == 0:
        return f"gsSPSetGeometryMode({set_params})", 0
    return f"gsSPGeometryMode({clr_params}, {set_params})", 0

def g_popmtx(ctx: GfxCtx):
    n = ctx.w1 // 64
    return f"gsSPPopMatrix({n})", 0

def g_texture(ctx: GfxCtx):
    s = C(ctx.w1, 16, 16)
    t = C(ctx.w1, 0, 16)
    level = C(ctx.w0, 11, 3)
    tile = C(ctx.w0, 8, 3)
    tile_str = G_TEXTURE_TILES.get(tile, f"{tile}")
    on = C(ctx.w0, 1, 7)
    on_str = G_ON_OFF.get(on, f"{on}")
    return f"gsSPTexture(0x{s:04X}, 0x{t:04X}, {level}, {tile_str}, {on_str})", 0

def g_copymem(ctx: GfxCtx):
    src = (C(ctx.w0, 16, 8) * 8) // 24 - 1
    dst = (C(ctx.w0, 8, 8) * 8) // 24 - 1
    part = src // 2 - 1
    part_str = G_COPYMEM_BODY_PARTS.get(part, f"{part}")
    if C(ctx.w(1, 0), 24, 8) == G_COPYMEM:
        return f"gsSPCopyLightsPlayerPart({part_str})", 1
    # NOTE: DynOS doesn't actually know how to decode this
    # sub_part = 1 + (src + 1) % 2
    # return f"gsSPCopyLightEXT({dst}, ((2 * (({part_str}) + 1)) + {sub_part}))", 0
    return f"gsSPCopyLightEXT({dst}, {src})", 0

def g_vtx(ctx: GfxCtx):
    v = ctx.w1
    n = C(ctx.w0, 12, 8)
    v0 = C(ctx.w0, 1, 7) - n
    return f"gsSPVertex({v}, {n}, {v0})", 0

def g_tri1(ctx: GfxCtx):
    v0 = C(ctx.w0, 16, 8) // 2
    v1 = C(ctx.w0, 8, 8) // 2
    v2 = C(ctx.w0, 0, 8) // 2
    return f"gsSP1Triangle({v0}, {v1}, {v2}, 0x0)", 0

def g_tri2(ctx: GfxCtx):
    v00 = C(ctx.w0, 16, 8) // 2
    v01 = C(ctx.w0, 8, 8) // 2
    v02 = C(ctx.w0, 0, 8) // 2
    v10 = C(ctx.w1, 16, 8) // 2
    v11 = C(ctx.w1, 8, 8) // 2
    v12 = C(ctx.w1, 0, 8) // 2
    return f"gsSP2Triangles({v00}, {v01}, {v02}, 0x0, {v10}, {v11}, {v12}, 0x0)", 0

#
# RDP commands
#

def g_setcombine(ctx: GfxCtx):
    a0 = G_SETCOMBINE_COLOR_COMBINERS["a"].get(C(ctx.w0, 20, 4), "0")
    b0 = G_SETCOMBINE_COLOR_COMBINERS["b"].get(C(ctx.w1, 28, 4), "0")
    c0 = G_SETCOMBINE_COLOR_COMBINERS["c"].get(C(ctx.w0, 15, 5), "0")
    d0 = G_SETCOMBINE_COLOR_COMBINERS["d"].get(C(ctx.w1, 15, 3), "0")
    Aa0 = G_SETCOMBINE_ALPHA_COMBINERS["a"].get(C(ctx.w0, 12, 3), "0")
    Ab0 = G_SETCOMBINE_ALPHA_COMBINERS["b"].get(C(ctx.w1, 12, 3), "0")
    Ac0 = G_SETCOMBINE_ALPHA_COMBINERS["c"].get(C(ctx.w0, 9, 3), "0")
    Ad0 = G_SETCOMBINE_ALPHA_COMBINERS["d"].get(C(ctx.w1, 9, 3), "0")
    a1 = G_SETCOMBINE_COLOR_COMBINERS["a"].get(C(ctx.w0, 5, 4), "0")
    b1 = G_SETCOMBINE_COLOR_COMBINERS["b"].get(C(ctx.w1, 24, 4), "0")
    c1 = G_SETCOMBINE_COLOR_COMBINERS["c"].get(C(ctx.w0, 0, 5), "0")
    d1 = G_SETCOMBINE_COLOR_COMBINERS["d"].get(C(ctx.w1, 6, 3), "0")
    Aa1 = G_SETCOMBINE_ALPHA_COMBINERS["a"].get(C(ctx.w1, 21, 3), "0")
    Ab1 = G_SETCOMBINE_ALPHA_COMBINERS["b"].get(C(ctx.w1, 3, 3), "0")
    Ac1 = G_SETCOMBINE_ALPHA_COMBINERS["c"].get(C(ctx.w1, 18, 3), "0")
    Ad1 = G_SETCOMBINE_ALPHA_COMBINERS["d"].get(C(ctx.w1, 0, 3), "0")
    cycle1 = f"{a0}, {b0}, {c0}, {d0}, {Aa0}, {Ab0}, {Ac0}, {Ad0}"
    cycle2 = f"{a1}, {b1}, {c1}, {d1}, {Aa1}, {Ab1}, {Ac1}, {Ad1}"
    cm1 = G_SETCOMBINE_MODES.get(cycle1)
    cm2 = G_SETCOMBINE_MODES.get(cycle2)
    if cm1 and cm2:
        return f"gsDPSetCombineMode({cm1}, {cm2})", 0
    return f"gsDPSetCombineLERP({cycle1}, {cycle2})", 0

def get_setimg_params(ctx: GfxCtx):
    fmt = C(ctx.w0, 21, 3)
    fmt_str = G_SETIMG_FMT.get(fmt, f"{fmt}")
    siz = C(ctx.w0, 19, 2)
    siz_str = G_SETIMG_SIZ.get(siz, f"{siz}")
    width = C(ctx.w0, 0, 12) + 1
    img, _ = get_pointer_and_offset(ctx.w1)
    return fmt_str, siz_str, width, img

def g_setcimg(ctx: GfxCtx):
    f, s, w, i = get_setimg_params(ctx)
    return f"gsDPSetColorImage({f}, {s}, {w}, {i})", 0

def g_setzimg(ctx: GfxCtx):
    f, s, w, i = get_setimg_params(ctx)
    return f"gsDPSetDepthImage({i})", 0

def g_settimg(ctx: GfxCtx):
    f, s, w, i = get_setimg_params(ctx)
    return f"gsDPSetTextureImage({f}, {s}, {w}, {i})", 0

def get_setcolor_params(ctx: GfxCtx):
    color = C(ctx.w1, 0, 32)
    r = C(color, 24, 8)
    g = C(color, 16, 8)
    b = C(color, 8, 8)
    a = C(color, 0, 8)
    return color, r, g, b, a

def g_setenvcolor(ctx: GfxCtx):
    _, r, g, b, a = get_setcolor_params(ctx)
    return f"gsDPSetEnvColor({r}, {g}, {b}, {a})", 0

def g_setprimcolor(ctx: GfxCtx):
    _, r, g, b, a = get_setcolor_params(ctx)
    m = C(ctx.w0, 8, 8)
    l = C(ctx.w0, 0, 8)
    return f"gsDPSetPrimColor({m}, {l}, {r}, {g}, {b}, {a})", 0

def g_setblendcolor(ctx: GfxCtx):
    _, r, g, b, a = get_setcolor_params(ctx)
    return f"gsDPSetBlendColor({r}, {g}, {b}, {a})", 0

def g_setfogcolor(ctx: GfxCtx):
    _, r, g, b, a = get_setcolor_params(ctx)
    return f"gsDPSetFogColor({r}, {g}, {b}, {a})", 0

def g_setfillcolor(ctx: GfxCtx):
    color, _, _, _, _ = get_setcolor_params(ctx)
    return f"gsDPSetFillColor(0x{color:08X})", 0

def g_fillrect(ctx: GfxCtx):
    ulx = C(ctx.w1, 16, 16)
    uly = C(ctx.w0, 12, 12)
    lrx = C(ctx.w1, 0, 16)
    lry = C(ctx.w0, 0, 12)
    return f"gsDPFillRectangle({ulx}, {uly}, {lrx}, {lry})", 0

def g_settile(ctx: GfxCtx):
    fmt = C(ctx.w0, 21, 3)
    fmt_str = G_SETTILE_FMT.get(fmt, f"{fmt}")
    siz = C(ctx.w0, 19, 2)
    siz_str = G_SETTILE_SIZ.get(siz, f"{siz}")
    line = C(ctx.w0, 9, 9)
    tmem = C(ctx.w0, 0, 9)
    tile = C(ctx.w1, 24, 3)
    tile_str = G_SETTILE_TILES.get(tile, f"{tile}")
    palette = C(ctx.w1, 20, 4)
    cmt = C(ctx.w1, 18, 2)
    cmt_params = get_named_flags(cmt, G_SETTILE_FLAGS)
    maskt = C(ctx.w1, 14, 4)
    shiftt = C(ctx.w1, 10, 4)
    cms = C(ctx.w1, 8, 2)
    cms_params = get_named_flags(cms, G_SETTILE_FLAGS)
    masks = C(ctx.w1, 4, 4)
    shifts = C(ctx.w1, 0, 4)
    return f"gsDPSetTile({fmt_str}, {siz_str}, {line}, {tmem}, {tile_str}, {palette}, {cmt_params}, {maskt}, {shiftt}, {cms_params}, {masks}, {shifts})", 0

def g_loadtile(ctx: GfxCtx):
    tile = C(ctx.w1, 24, 3)
    tile_str = G_LOADTILE_TILES.get(tile, f"{tile}")
    uls = C(ctx.w0, 12, 12)
    ult = C(ctx.w0, 0, 12)
    lrs = C(ctx.w1, 12, 12)
    lrt = C(ctx.w1, 0, 12)
    return f"gsDPLoadTile({tile_str}, {uls}, {ult}, {lrs}, {lrt})", 0

def g_loadblock(ctx: GfxCtx):
    tile = C(ctx.w1, 24, 3)
    tile_str = G_LOADBLOCK_TILES.get(tile, f"{tile}")
    uls = C(ctx.w0, 12, 12)
    ult = C(ctx.w0, 0, 12)
    lrs = C(ctx.w1, 12, 12)
    dxt = C(ctx.w1, 0, 12)
    return f"gsDPLoadBlock({tile_str}, {uls}, {ult}, {lrs}, {dxt})", 0

def g_settilesize(ctx: GfxCtx):
    tile = C(ctx.w1, 24, 3)
    tile_str = G_SETTILESIZE_TILES.get(tile, f"{tile}")
    uls = C(ctx.w0, 12, 12)
    ult = C(ctx.w0, 0, 12)
    lrs = C(ctx.w1, 12, 12)
    lrt = C(ctx.w1, 0, 12)
    return f"gsDPSetTileSize({tile_str}, {uls}, {ult}, {lrs}, {lrt})", 0

def g_loadtlut(ctx: GfxCtx):
    tile = C(ctx.w1, 24, 3)
    tile_str = G_LOADTLUT_TILES.get(tile, f"{tile}")
    count = C(ctx.w1, 14, 10)
    return f"gsDPLoadTLUTCmd({tile_str}, {count})", 0

def g_setscissor(ctx: GfxCtx):
    mode = C(ctx.w1, 24, 2)
    mode_str = G_SETSCISSOR_MODES.get(mode, f"{mode}")
    ulx = C(ctx.w0, 12, 12) // 4
    uly = C(ctx.w0, 0, 12) // 4
    lrx = C(ctx.w1, 12, 12) // 4
    lry = C(ctx.w1, 0, 12) // 4
    return f"gsDPSetScissor({mode_str}, {ulx}, {uly}, {lrx}, {lry})", 0

def g_rdpfullsync(ctx: GfxCtx):
    return f"gsDPFullSync()", 0

def g_rdptilesync(ctx: GfxCtx):
    return f"gsDPTileSync()", 0

def g_rdppipesync(ctx: GfxCtx):
    return f"gsDPPipeSync()", 0

def g_rdploadsync(ctx: GfxCtx):
    return f"gsDPLoadSync()", 0

def g_texrectflip(ctx: GfxCtx):
    xl = C(ctx.w1, 21, 11) << 2
    yl = C(ctx.w1, 12, 9) << 2
    xh = C(ctx.w0, 13, 11) << 2
    yh = C(ctx.w0, 4, 9) << 2
    dsdx = C(ctx.w1, 4, 8) << 6
    dtdy = (C(ctx.w1, 0, 4) << 10) | (C(ctx.w0, 0, 4) << 6)
    return f"gsSPTextureRectangleFlip({xl}, {yl}, {xh}, {yh}, 0, 0, 0, {dsdx}, {dtdy})", 0

def g_texrect(ctx: GfxCtx):
    xl = C(ctx.w1, 21, 11) << 2
    yl = C(ctx.w1, 12, 9) << 2
    xh = C(ctx.w0, 13, 11) << 2
    yh = C(ctx.w0, 4, 9) << 2
    dsdx = C(ctx.w1, 4, 8) << 6
    dtdy = (C(ctx.w1, 0, 4) << 10) | (C(ctx.w0, 0, 4) << 6)
    return f"gsSPTextureRectangle({xl}, {yl}, {xh}, {yh}, 0, 0, 0, {dsdx}, {dtdy})", 0

#
# Extended commands
#

def g_vtx_ext(ctx: GfxCtx):
    v = ctx.w1
    n = C(ctx.w0, 12, 8)
    v0 = C(ctx.w0, 1, 7) - n
    return f"gsSPVertexNonGlobal({v}, {n}, {v0})", 0

def g_tri2_ext(ctx: GfxCtx):
    v00 = C(ctx.w0, 16, 8) // 2
    v01 = C(ctx.w0, 8, 8) // 2
    v02 = C(ctx.w0, 0, 8) // 2
    v10 = C(ctx.w1, 16, 8) // 2
    v11 = C(ctx.w1, 8, 8) // 2
    v12 = C(ctx.w1, 0, 8) // 2
    return f"gsSP2TrianglesDjui({v00}, {v01}, {v02}, 0x0, {v10}, {v11}, {v12}, 0x0)", 0

def g_pparttocolor(ctx: GfxCtx):
    color = C(ctx.w0, 16, 8)
    color_str = G_PPARTTOCOLOR_COLORS.get(color, f"{color}")
    offset = (ctx.w1 - 1) & 1
    offset_str = G_PPARTTOCOLOR_OFFSETS.get(offset, f"{offset}")
    part = ((ctx.w1 - offset - 1) / 2) - 1
    part_str = G_PPARTTOCOLOR_BODY_PARTS.get(part, f"{part}")
    return f"gsSPCopyPlayerPartToColor({color_str}, {part_str}, {offset_str})", 0

#
# GFX commands
#

GFX_COMMANDS = {

# RSP
    G_NOOP: g_noop,
    G_SETOTHERMODE_H: lambda ctx: g_setothermode(ctx, "G_SETOTHERMODE_H", G_SETOTHERMODE_H_SHIFTS),
    G_SETOTHERMODE_L: lambda ctx: g_setothermode(ctx, "G_SETOTHERMODE_L", G_SETOTHERMODE_L_SHIFTS),
    G_SPNOOP: g_spnoop,
    G_ENDDL: g_enddl,
    G_DL: g_dl,
    G_MOVEMEM: g_movemem,
    G_MOVEWORD: g_moveword,
    G_MTX: g_mtx,
    G_GEOMETRYMODE: g_geometrymode,
    G_POPMTX: g_popmtx,
    G_TEXTURE: g_texture,
    G_COPYMEM: g_copymem,
    G_VTX: g_vtx,
    G_TRI1: g_tri1,
    G_TRI2: g_tri2,

# RDP
    G_SETCIMG: g_setcimg,
    G_SETZIMG: g_setzimg,
    G_SETTIMG: g_settimg,
    G_SETCOMBINE: g_setcombine,
    G_SETENVCOLOR: g_setenvcolor,
    G_SETPRIMCOLOR: g_setprimcolor,
    G_SETBLENDCOLOR: g_setblendcolor,
    G_SETFOGCOLOR: g_setfogcolor,
    G_SETFILLCOLOR: g_setfillcolor,
    G_FILLRECT: g_fillrect,
    G_SETTILE: g_settile,
    G_LOADTILE: g_loadtile,
    G_LOADBLOCK: g_loadblock,
    G_SETTILESIZE: g_settilesize,
    G_LOADTLUT: g_loadtlut,
    G_SETSCISSOR: g_setscissor,
    G_RDPFULLSYNC: g_rdpfullsync,
    G_RDPTILESYNC: g_rdptilesync,
    G_RDPPIPESYNC: g_rdppipesync,
    G_RDPLOADSYNC: g_rdploadsync,
    G_TEXRECTFLIP: g_texrectflip,
    G_TEXRECT: g_texrect,

# Extended
    G_VTX_EXT: g_vtx_ext,
    G_TRI2_EXT: g_tri2_ext,
    G_PPARTTOCOLOR: g_pparttocolor,
}


@GfxData.writer()
def write_model_inc_c(self: GfxData, dirpath: str, model_name: str):
    with open(os.path.join(dirpath, "model.inc.c"), "w", newline="\n") as models_inc_c:

        # Write lights
        for name, light in self.lights.items():
            models_inc_c.write("Light_t %s[] = {{{0x%02X, 0x%02X, 0x%02X}, 0, {0x%02X, 0x%02X, 0x%02X}, 0, {%d, %d, %d}, 0}};" % (
                name, light.cr, light.cg, light.cb, light.c2r, light.c2g, light.c2b, light.dx, light.dy, light.dz
            ))
            models_inc_c.write("\n\n")

        for name, ambient in self.ambients.items():
            models_inc_c.write("Ambient_t %s[] = {{{0x%02X, 0x%02X, 0x%02X}, 0, {0x%02X, 0x%02X, 0x%02X}, 0}};" % (
                name, ambient.cr, ambient.cg, ambient.cb, ambient.c2r, ambient.c2g, ambient.c2b
            ))
            models_inc_c.write("\n\n")

        for name, lights1 in self.lights1.items():
            models_inc_c.write("Lights1 %s = gdSPDefLights1(0x%02X, 0x%02X, 0x%02X, 0x%02X, 0x%02X, 0x%02X, 0x%02X, 0x%02X, 0x%02X);" % (
                name, lights1.ar, lights1.ag, lights1.ab, lights1.r1, lights1.g1, lights1.b1, lights1.x1, lights1.y1, lights1.z1
            ))
            models_inc_c.write("\n\n")

        # Write textures
        for name, texture in self.textures.items():
            if texture.ref or texture.write(os.path.join(dirpath, name + ".png")):
                models_inc_c.write("Texture %s[] = \"actors/%s/%s\";" % (
                    name, model_name, texture.ref or name
                ))
            else: # Empty or corrupted texture
                models_inc_c.write("Texture %s[] = {0};" % (name))
            models_inc_c.write("\n\n")

        # Write vertex arrays
        for name, vtxarr in self.vertices.items():
            models_inc_c.write("Vtx %s[] = {\n" % (name))
            for vtx in vtxarr.buffer:
                models_inc_c.write("    {{{%d, %d, %d}, 0x%X, {%d, %d}, {0x%02X, 0x%02X, 0x%02X, 0x%02X}}},\n" % (
                    vtx.x, vtx.y, vtx.z, vtx.f, vtx.u, vtx.v, vtx.r, vtx.g, vtx.b, vtx.a
                ))
            models_inc_c.write("};\n\n")

        # Write display lists
        for name, displaylist in self.displaylists.items():
            models_inc_c.write("Gfx %s[] = {\n" % (name))
            i = 0
            while i < len(displaylist.buffer):
                ctx = GfxCtx(displaylist.buffer[i:], self)
                op = C(ctx.w0, 24, 8)
                cmd = GFX_COMMANDS.get(op)
                if cmd:
                    line, skip = cmd(ctx)
                    models_inc_c.write(f"    {line},\n")
                    i += skip * 2
                else:
                    models_inc_c.write(f"RAW_WORDS(0x{ctx.w0:08X}, {ctx.w1 if isinstance(ctx.w1, str) else f'0x{ctx.w1:08X}'}),\n")
                    prints.warning(f"Unknown gfx command: {ctx.w0:08X} {ctx.w1 if isinstance(ctx.w1, str) else f'{ctx.w1:08X}'} [{name}:0x{i//2:04X}]")
                i += 2
            models_inc_c.write("};\n\n")
