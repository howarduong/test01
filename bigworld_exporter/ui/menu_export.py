# bigworld_exporter/ui/menu_export.py

import bpy

class BW_MT_export_menu(bpy.types.Menu):
    bl_label = "BigWorld Export"
    bl_idname = "BW_MT_export_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("bw.export_model", text="Model/Visual/Primitives")
        layout.operator("bw.export_anim", text="Animation")
        layout.operator("bw.pack_assets", text="Full Pipeline")

def draw_export_menu(self, ctx):
    self.layout.menu(BW_MT_export_menu.bl_idname)

def register_ui():
    bpy.utils.register_class(BW_MT_export_menu)
    bpy.types.TOPBAR_MT_file_export.append(draw_export_menu)

def unregister_ui():
    bpy.types.TOPBAR_MT_file_export.remove(draw_export_menu)
    bpy.utils.unregister_class(BW_MT_export_menu)
