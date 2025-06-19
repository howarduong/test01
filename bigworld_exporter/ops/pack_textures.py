# bigworld_exporter/ops/pack_textures.py

import os, traceback
import bpy
from bpy.types import Operator
from ..utils import bw_texture_packer, bw_logging

logger = bw_logging.get_logger()

class BW_OT_pack_textures(Operator):
    bl_idname = "bw.pack_textures"
    bl_label = "Pack Textures"
    bl_description = "Generate texture atlases and compress textures"
    bl_options = {'REGISTER'}

    def execute(self, context):
        s = context.scene.bw_export
        root = bpy.path.abspath(s.resource_root)
        try:
            logger.info("Packing textures...")
            bw_texture_packer.pack(root, compress=s.tex_compress)
            self.report({'INFO'}, "Textures packed")
            return {'FINISHED'}
        except Exception as e:
            logger.error("Texture packing failed", exc_info=True)
            self.report({'ERROR'}, f"Texture packing failed: {e}")
            return {'CANCELLED'}

def register_pack_textures():
    bpy.utils.register_class(BW_OT_pack_textures)

def unregister_pack_textures():
    bpy.utils.unregister_class(BW_OT_pack_textures)
