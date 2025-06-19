# bigworld_exporter/ui/panel_resources.py

import bpy
import os
from bpy.types import UIList
from ..properties import BWExportSettings

def register_resources_ui():
    bpy.utils.register_class(BW_UL_resources)
    bpy.utils.register_class(BW_PT_resources)

def unregister_resources_ui():
    bpy.utils.unregister_class(BW_PT_resources)
    bpy.utils.unregister_class(BW_UL_resources)

class BW_UL_resources(UIList):
    """List all exported BigWorld assets in resource_root"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        fp = item
        name = os.path.basename(fp.filepath)
        layout.label(text=name, icon='FILE')

class BW_PT_resources(bpy.types.Panel):
    bl_idname = "BW_PT_resources"
    bl_label = "5. Resource Browser"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BigWorld'

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def draw(self, context):
        s = context.scene.bw_export
        layout = self.layout
        root = bpy.path.abspath(s.resource_root)
        layout.label(text="Exported Assets", icon='FILE_FOLDER')
        if not os.path.isdir(root):
            layout.label(text="Invalid resource root", icon='ERROR')
            return
        files = sorted(os.listdir(root))
        wl = layout.template_list("BW_UL_resources", "", context.scene, "bw_export_list", context.scene, "bw_export_index", rows=5)
        # we populate these properties in pack_assets operator or via update callback
