# bigworld_exporter/ui/panel_model.py

import bpy
from ..properties import BWExportSettings
from ..ops.export_model import BW_OT_export_model

def register_model_ui():
    bpy.utils.register_class(BW_PT_model_export)

def unregister_model_ui():
    bpy.utils.unregister_class(BW_PT_model_export)

class BW_PT_model_export(bpy.types.Panel):
    bl_idname = "BW_PT_model_export"
    bl_label = "2. Model & Visual Export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BigWorld'

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def draw(self, context):
        s = context.scene.bw_export
        layout = self.layout

        layout.label(text="Chunk Settings", icon='MESH_DATA')
        row = layout.row(align=True)
        row.prop(s, "max_verts")
        row.prop(s, "max_indices")
        layout.prop(s, "grouping")

        layout.separator()
        layout.label(text="Vertex Attributes")
        row = layout.row(align=True)
        row.prop(s, "include_normals")
        row.prop(s, "include_tangents")
        row = layout.row(align=True)
        row.prop(s, "include_uvs")
        row.prop(s, "include_vcolor")
        layout.prop(s, "include_skin")

        layout.separator()
        layout.label(text="Collision & Primitives")
        row = layout.row(align=True)
        row.prop(s, "export_primitives")
        row.prop(s, "collision_type")
        if s.export_primitives:
            layout.prop(s, "collision_filter")

        layout.separator()
        layout.label(text="Materials")
        layout.prop(s, "export_materials")

        layout.separator()
        layout.operator(BW_OT_export_model.bl_idname, icon='EXPORT', text="Export Model/Visual/Primitives")
