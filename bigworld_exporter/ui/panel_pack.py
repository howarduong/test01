# bigworld_exporter/ui/panel_pack.py

import bpy
from ..properties import BWExportSettings
from ..ops.pack_textures import BW_OT_pack_textures
from ..ops.pack_assets import BW_OT_pack_assets

def register_pack_ui():
    bpy.utils.register_class(BW_PT_pack)

def unregister_pack_ui():
    bpy.utils.unregister_class(BW_PT_pack)

class BW_PT_pack(bpy.types.Panel):
    bl_idname = "BW_PT_pack"
    bl_label = "4. Packing & Pipeline"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BigWorld'

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def draw(self, context):
        prefs = context.preferences.addons["bigworld_exporter"].preferences
        s = context.scene.bw_export
        layout = self.layout

        layout.label(text="Texture Packing", icon='IMAGE_DATA')
        row = layout.row(align=True)
        row.prop(s, "tex_compress")
        layout.operator(BW_OT_pack_textures.bl_idname, text="Pack Textures")

        layout.separator()
        layout.label(text="Post-Export Pipeline", icon='NODETREE')
        col = layout.column(align=True)
        col.prop(s, "post_tools")
        box = col.box()
        box.enabled = s.post_tools
        box.label(text="External Tools Paths:")
        box.prop(prefs, "convert_model_script")
        box.prop(prefs, "convert_materials_script")
        box.prop(prefs, "texture_tool_executable")
        box.prop(prefs, "package_builder_script")
        box.prop(prefs, "chunk_viz_script")
        box.prop(prefs, "resource_scanner_script")

        layout.operator(BW_OT_pack_assets.bl_idname, text="Run Full Pipeline")
