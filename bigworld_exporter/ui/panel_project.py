# bigworld_exporter/ui/panel_project.py

import bpy, os
from ..properties import BWExportSettings
from ..ops.project_init import BW_OT_project_wizard

def register_project_ui():
    bpy.utils.register_class(BW_PT_project_setup)

def unregister_project_ui():
    bpy.utils.unregister_class(BW_PT_project_setup)

class BW_PT_project_setup(bpy.types.Panel):
    bl_idname = "BW_PT_project_setup"
    bl_label = "1. Project Setup"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BigWorld'

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        prefs = context.preferences.addons["bigworld_exporter"].preferences
        # 防御性初始化，确保 settings 可用
        if not hasattr(context.scene, "bw_export") or context.scene.bw_export is None:
            context.scene.bw_export = bpy.context.scene.bw_export
        settings = context.scene.bw_export

        layout.label(text="External Tools Paths:", icon='PREFERENCES')
        col = layout.column(align=True)
        col.prop(prefs, "convert_model_script")
        col.prop(prefs, "convert_materials_script")
        col.prop(prefs, "texture_tool_executable")

        layout.separator()
        layout.label(text="Project Export Root:", icon='FILE_FOLDER')
        row = layout.row()
        row.prop(settings, "resource_root", text="")  # 只显示输入框和文件选择按钮，提升显示宽度

        layout.separator()
        layout.operator(BW_OT_project_wizard.bl_idname, icon='FILE_NEW', text="Create Project Structure")
