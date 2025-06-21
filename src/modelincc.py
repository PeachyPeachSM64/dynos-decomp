import os
from .gfxdata import GfxData


BODY_PARTS = [
    "PANTS",
    "SHIRT",
    "GLOVES",
    "SHOES",
    "HAIR",
    "SKIN",
    "CAP",
    "EMBLEM",
]


# TODO: this is really bad, but works most of the time
def write_display_list_words(models_inc_c, w0, w1):
    cmd = ((w0 >> 24) & 0xFF)

    # gsSPDisplayList
    if w0 == 0xDE000000:
        return models_inc_c.write("    gsSPDisplayList(%s),\n" % (w1))

    # gsSPEndDisplayList
    if cmd == 0xDF:
        return models_inc_c.write("    gsSPEndDisplayList(),\n")

    # gsDPLoadSync
    if cmd == 0xE6:
        return models_inc_c.write("    gsDPLoadSync(),\n")

    # gsDPPipeSync
    if cmd == 0xE7:
        return models_inc_c.write("    gsDPPipeSync(),\n")

    # gsDPTileSync
    if cmd == 0xE8:
        return models_inc_c.write("    gsDPTileSync(),\n")

    # gsDPFullSync
    if cmd == 0xE9:
        return models_inc_c.write("    gsDPFullSync(),\n")

    # gsSPVertex
    if cmd == 0x01:
        return models_inc_c.write("    gsSPVertex(%s, %d, %d),\n" % (
            w1,
            ((w0 >> 12) & 0xFF),
            ((w0 >> 1) & 0x7F) - ((w0 >> 12) & 0xFF)
        ))

    # gsSP1Triangle
    if cmd == 0x05:
        return models_inc_c.write("    gsSP1Triangle(%d, %d, %d, 0x0),\n" % (
            ((w0 >> 16) & 0xFF) // 2,
            ((w0 >> 8) & 0xFF) // 2,
            ((w0 >> 0) & 0xFF) // 2,
        ))

    # gsSP2Triangles
    if cmd == 0x06:
        return models_inc_c.write("    gsSP2Triangles(%d, %d, %d, 0x0, %d, %d, %d, 0x0),\n" % (
            ((w0 >> 16) & 0xFF) // 2,
            ((w0 >> 8) & 0xFF) // 2,
            ((w0 >> 0) & 0xFF) // 2,
            ((w1 >> 16) & 0xFF) // 2,
            ((w1 >> 8) & 0xFF) // 2,
            ((w1 >> 0) & 0xFF) // 2,
        ))

    # gsSPSetGeometryMode
    if cmd == 0xD9 and w1 != 0:
        return models_inc_c.write("    gsSPSetGeometryMode(0x%08X),\n" % (
            (w1 & 0xFFFFFFFF)
        ))

    # gsSPClearGeometryMode
    if cmd == 0xD9 and w1 == 0:
        return models_inc_c.write("    gsSPClearGeometryMode(0x%08X),\n" % (
            (~w0 & 0xFFFFFFFF)
        ))

    # gsDPSetCombine
    if cmd == 0xFC:
        return models_inc_c.write("    gsDPSetCombine(0x%08X, 0x%08X),\n" % (
            (w0 & 0x00FFFFFF),
            (w1 & 0xFFFFFFFF)
        ))

    # gsSPTexture
    if cmd == 0xD7:
        return models_inc_c.write("    gsSPTexture(0x%04X, 0x%04X, %d, %d, %d),\n" % (
            ((w1 >> 16) & 0xFFFF),
            ((w1 >> 0) & 0xFFFF),
            ((w0 >> 11) & 0x7),
            ((w0 >> 8) & 0x7),
            ((w0 >> 1) & 0x7F)
        ))

    # gsDPSetEnvColor
    if cmd == 0xFB:
        return models_inc_c.write("    gsDPSetEnvColor(0x%02X, 0x%02X, 0x%02X, 0x%02X),\n" % (
            ((w1 >> 24) & 0xFF),
            ((w1 >> 16) & 0xFF),
            ((w1 >> 8) & 0xFF),
            ((w1 >> 0) & 0xFF),
        ))

    # gsDPSetPrimColor
    if cmd == 0xFA:
        return models_inc_c.write("    gsDPSetPrimColor(0x%02X, 0x%02X, 0x%02X, 0x%02X, 0x%02X, 0x%02X),\n" % (
            ((w0 >> 8) & 0xFF),
            ((w0 >> 0) & 0xFF),
            ((w1 >> 24) & 0xFF),
            ((w1 >> 16) & 0xFF),
            ((w1 >> 8) & 0xFF),
            ((w1 >> 0) & 0xFF),
        ))

    # gsDPSetBlendColor
    if cmd == 0xF9:
        return models_inc_c.write("    gsDPSetBlendColor(0x%02X, 0x%02X, 0x%02X, 0x%02X),\n" % (
            ((w1 >> 24) & 0xFF),
            ((w1 >> 16) & 0xFF),
            ((w1 >> 8) & 0xFF),
            ((w1 >> 0) & 0xFF),
        ))

    # gsDPSetFogColor
    if cmd == 0xF8:
        return models_inc_c.write("    gsDPSetFogColor(0x%02X, 0x%02X, 0x%02X, 0x%02X),\n" % (
            ((w1 >> 24) & 0xFF),
            ((w1 >> 16) & 0xFF),
            ((w1 >> 8) & 0xFF),
            ((w1 >> 0) & 0xFF),
        ))

    # gsDPSetFillColor
    if cmd == 0xF7:
        return models_inc_c.write("    gsDPSetFillColor(0x%08x),\n" % (
            (w1 & 0xFFFFFFFF)
        ))

    # gsDPSetTextureImage
    if cmd == 0xFD:
        return models_inc_c.write("    gsDPSetTextureImage(%d, %d, %d, %s),\n" % (
            ((w0 >> 21) & 0x7),
            ((w0 >> 19) & 0x3),
            ((w0 >> 0) & 0xFFF) + 1,
            w1
        ))

    # gsDPLoadTile
    if cmd == 0xF4:
        return models_inc_c.write("    gsDPLoadTile(%d, %d, %d, %d, %d),\n" % (
            ((w1 >> 24) & 0x7),
            ((w0 >> 12) & 0xFFF),
            ((w0 >> 0) & 0xFFF),
            ((w1 >> 12) & 0xFFF),
            ((w1 >> 0) & 0xFFF),
        ))

    # gsDPSetTile
    if cmd == 0xF5:
        return models_inc_c.write("    gsDPSetTile(%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d),\n" % (
            ((w0 >> 21) & 0x7),
            ((w0 >> 19) & 0x3),
            ((w0 >> 9) & 0x1FF),
            ((w0 >> 0) & 0x1FF),
            ((w1 >> 24) & 0x7),
            ((w1 >> 20) & 0xF),
            ((w1 >> 18) & 0x3),
            ((w1 >> 14) & 0xF),
            ((w1 >> 10) & 0xF),
            ((w1 >> 8) & 0x3),
            ((w1 >> 4) & 0xF),
            ((w1 >> 0) & 0xF),
        ))

    # gsDPSetTileSize
    if cmd == 0xF2:
        return models_inc_c.write("    gsDPSetTileSize(%d, %d, %d, %d, %d),\n" % (
            ((w1 >> 24) & 0x7),
            ((w0 >> 12) & 0xFFF),
            ((w0 >> 0) & 0xFFF),
            ((w1 >> 12) & 0xFFF),
            ((w1 >> 0) & 0xFFF),
        ))

    # gsDPLoadBlock
    if cmd == 0xF3:
        return models_inc_c.write("    gsDPLoadBlock(%d, %d, %d, %d, %d),\n" % (
            ((w1 >> 24) & 0x7),
            ((w0 >> 12) & 0xFFF),
            ((w0 >> 0) & 0xFFF),
            ((w1 >> 12) & 0xFFF),
            ((w1 >> 0) & 0xFFF),
        ))

    # gsSPCopyLightEXT
    if cmd == 0xD2:
        dst = (((((w0 >> 8) & 0xFF) * 8) - 24) // 24)
        src = (((((w0 >> 16) & 0xFF) * 8) - 24) // 24)
        part = (((src - dst) // 2) - 1)
        return models_inc_c.write("    gsSPCopyLightsPlayerPart(%s),\n" % (
            BODY_PARTS[part],
        )) if dst == 1 else None

    # gsSPSetLights1
    if w0 == 0xDB020000:
        return models_inc_c.write("    gsSPSetLights1(")
    if w0 == 0xDC08060A:
        return models_inc_c.write("%s),\n" % (w1[:max(0, w1.find(" +"))]))
    if w0 == 0xDC08090A:
        return None

    # gsDPSetAlphaCompare(G_AC_NONE)
    if w0 == 0xE2001E01:
        return models_inc_c.write("    gsDPSetAlphaCompare(G_AC_NONE),\n")

    # Raw with pointer
    if isinstance(w1, str):
        return models_inc_c.write("RAW_WORDS(0x%08X, %s),\n" % (w0, w1))

    # Raw
    return models_inc_c.write("RAW_WORDS(0x%08X, 0x%08X),\n" % (w0, w1))


def write_model_inc_c(dirpath: str, model_name: str, gfxdata: GfxData):
    with open(os.path.join(dirpath, "model.inc.c"), "w", newline="\n") as models_inc_c:

        # Write lights
        for name, lights1 in gfxdata.lights1.items():
            models_inc_c.write("Lights1 %s = gdSPDefLights1(0x%02X, 0x%02X, 0x%02X, 0x%02X, 0x%02X, 0x%02X, 0x%02X, 0x%02X, 0x%02X);" % (
                name, lights1.ar, lights1.ag, lights1.ab, lights1.r1, lights1.g1, lights1.b1, lights1.x1, lights1.y1, lights1.z1
            ))
            models_inc_c.write("\n\n")

        # Write textures
        for name, texture in gfxdata.textures.items():
            models_inc_c.write("Texture %s[] = \"actors/%s/%s.rgba32\";" % (
                name, model_name, texture.ref or name
            ))
            models_inc_c.write("\n\n")
            if texture.png:
                open(os.path.join(dirpath, name + ".rgba32.png"), "wb").write(texture.png)

        # Write vertex arrays
        for name, vtxarr in gfxdata.vertices.items():
            models_inc_c.write("Vtx %s[] = {\n" % (name))
            for vtx in vtxarr.buffer:
                models_inc_c.write("    {{{%d, %d, %d}, 0x%X, {%d, %d}, {0x%02X, 0x%02X, 0x%02X, 0x%02X}}},\n" % (
                    vtx.x, vtx.y, vtx.z, vtx.f, vtx.u, vtx.v, vtx.r, vtx.g, vtx.b, vtx.a
                ))
            models_inc_c.write("};\n\n")

        # Write display lists
        for name, displaylist in gfxdata.displaylists.items():
            models_inc_c.write("Gfx %s[] = {\n" % (name))
            for i in range(0, len(displaylist.buffer), 2):
                w0 = displaylist.buffer[i + 0]
                w1 = displaylist.buffer[i + 1]
                write_display_list_words(models_inc_c, w0, w1)
            models_inc_c.write("};\n\n")
