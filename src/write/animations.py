import os
from ..gfxdata import GfxData


@GfxData.writer()
def write_animations(self: GfxData, dirpath: str):
    if self.animations:
        os.makedirs(os.path.join(dirpath, "anims"), exist_ok=True)
        for anim_name, animation in self.animations.items():
            with open(os.path.join(dirpath, "anims/%s.inc.c" % (anim_name)), "w", newline="\n") as anim_inc_c:
                anim_inc_c.write("static const struct Animation %s = {\n" % (anim_name))
                anim_inc_c.write("    %d,\n" % (animation.flags))
                anim_inc_c.write("    %d,\n" % (animation.anim_y_trans_div))
                anim_inc_c.write("    %d,\n" % (animation.start_frame))
                anim_inc_c.write("    %d,\n" % (animation.loop_start))
                anim_inc_c.write("    %d,\n" % (animation.loop_end))
                anim_inc_c.write("    ANIMINDEX_NUMPARTS(%s_index),\n" % (anim_name))
                anim_inc_c.write("    %s_value,\n" % (anim_name))
                anim_inc_c.write("    %s_index,\n" % (anim_name))
                anim_inc_c.write("    %d,\n" % (animation.length))
                anim_inc_c.write("};\n")
                anim_inc_c.write("\n")
                anim_inc_c.write("static const u16 %s_index[] = {" % (anim_name))
                for i, index in enumerate(animation.index):
                    if i % 8 == 0: anim_inc_c.write("\n   ")
                    anim_inc_c.write(" 0x%04X," % (index))
                anim_inc_c.write("\n};\n")
                anim_inc_c.write("\n")
                anim_inc_c.write("static const s16 %s_value[] = {" % (anim_name))
                for i, value in enumerate(animation.values):
                    if i % 8 == 0: anim_inc_c.write("\n   ")
                    anim_inc_c.write(" 0x%04X," % ((value + 0x10000) & 0xFFFF))
                anim_inc_c.write("\n};\n")


@GfxData.writer()
def write_animation_table(self: GfxData, dirpath: str):
    if self.animation_table:
        os.makedirs(os.path.join(dirpath, "anims"), exist_ok=True)
        with open(os.path.join(dirpath, "anims/table.inc.c"), "w", newline="\n") as table_inc_c:
            table_inc_c.write("const struct Animation *const anims[] = {\n")
            for anim_name in self.animation_table:
                table_inc_c.write("    %s%s,\n" % ("&" if anim_name != "NULL" else "", anim_name))
            table_inc_c.write("};\n")
