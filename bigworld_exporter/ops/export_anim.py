# bigworld_exporter/ops/export_anim.py

import os, traceback
import bpy
from bpy.types import Operator
from ..properties import BWExportSettings
from ..utils import (
    bw_xml_writer, bw_bin_writer, bw_morph, bw_logging
)

logger = bw_logging.get_logger()

class BW_OT_export_anim(Operator):
    bl_idname = "bw.export_anim"
    bl_label = "Export Animation"
    bl_description = "Export selected armatures and morph targets to BigWorld animation"
    bl_options = {'REGISTER'}

    def execute(self, context):
        s: BWExportSettings = context.scene.bw_export
        root = bpy.path.abspath(s.resource_root)
        os.makedirs(root, exist_ok=True)
        wm = context.window_manager

        try:
            start, end = (
                (context.scene.frame_start, context.scene.frame_end)
                if s.anim_range=='SCENE'
                else (s.custom_start, s.custom_end)
            )
            fps = s.anim_fps
            arms = [o for o in context.selected_objects if o.type=='ARMATURE']
            total = len(arms)
            wm.progress_begin(0, total)

            for i, arm in enumerate(arms):
                anim_writer = bw_xml_writer.AnimWriter(root, arm.name, fps, start, end)
                bone_list = arm.data.bones
                for f in range(start, end+1):
                    context.scene.frame_set(f)
                    for bone in bone_list:
                        mat = arm.matrix_world @ bone.matrix_local
                        anim_writer.write_bone_frame(bone.name, mat)
                anim_writer.save()
                if s.morphs:
                    for child in arm.children:
                        if child.type=='MESH' and child.data.shape_keys:
                            bw_morph.export(child, start, end, root)
                wm.progress_update(i+1)

            wm.progress_end()
            context.scene.frame_set(context.scene.frame_current)
            self.report({'INFO'}, "Animation export complete")
            return {'FINISHED'}

        except Exception as e:
            wm.progress_end()
            logger.error("Animation export failed", exc_info=True)
            self.report({'ERROR'}, f"Export failed: {e}")
            return {'CANCELLED'}

def register_export_anim():
    bpy.utils.register_class(BW_OT_export_anim)

def unregister_export_anim():
    bpy.utils.unregister_class(BW_OT_export_anim)
