# bigworld_exporter/ui/panel_anim.py

import bpy
from ..properties import BWExportSettings
from ..ops.export_anim import BW_OT_export_anim

def register_anim_ui():
    bpy.utils.register_class(BW_PT_anim_export)

def unregister_anim_ui():
    bpy.utils.unregister_class(BW_PT_anim_export)

class BW_PT_anim_export(bpy.types.Panel):
    bl_idname = "BW_PT_anim_export"
    bl_label = "3. Animation Export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BigWorld'

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def draw(self, context):
        s = context.scene.bw_export
        layout = self.layout

        layout.label(text="Frame Range", icon='TIME')
        row = layout.row(align=True)
        row.prop(s, "anim_range", expand=True)
        if s.anim_range == 'CUSTOM':
            col = layout.column(align=True)
            col.prop(s, "custom_start"); col.prop(s, "custom_end")

        layout.prop(s, "anim_fps")

        layout.separator()
        layout.prop(s, "morphs", text="Export Morph Targets")

        layout.separator()
        layout.operator(BW_OT_export_anim.bl_idname, icon='ANIM', text="Export Animation")
