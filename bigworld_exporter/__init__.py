# bigworld_exporter/__init__.py


# from .version import version_str  # 不要在 bl_info 里调用

bl_info = {
    "name":        "BigWorld Exporter",
    "author":      "Your Name",
    "version":     (0, 1, 0),          # ← 直接写字面量 tuple
    "blender":     (4, 5, 0),          
    "location":    "3D Viewport > Sidebar > BigWorld Exporter",
    "description": "Export models, visuals, primitives, animations for BigWorld Engine",
    "warning":     "",
    "doc_url":     "",
    "tracker_url": "",
    "category":    "Import-Export",
}

ADDON_NAME = "bigworld_exporter" # "bigworld_exporter"

import bpy
from .version import VERSION, version_str
from .preferences import BigWorldExporterPreferences
from .properties import BWExportSettings, BWExportItem
from .ui.menu_export import register_ui, unregister_ui
from .ui.panel_project import register_project_ui, unregister_project_ui
from .ui.panel_model import register_model_ui, unregister_model_ui
from .ui.panel_anim import register_anim_ui, unregister_anim_ui
from .ui.panel_pack import register_pack_ui, unregister_pack_ui
from .ui.panel_resources import register_resources_ui, unregister_resources_ui
from .ops.batch_cli import register_cli, unregister_cli
from .ops.project_init import register_project_ops, unregister_project_ops
from .ops.create_objects import register_create_ops, unregister_create_ops
from .ops.export_model import register_export_model, unregister_export_model
from .ops.export_anim import register_export_anim, unregister_export_anim
from .ops.pack_textures import register_pack_textures, unregister_pack_textures
from .ops.pack_assets import register_pack_assets, unregister_pack_assets
from .ops.import_bw import register_import_bw, unregister_import_bw
from .workflows import register_workflows, unregister_workflows

classes = (
    BigWorldExporterPreferences,
    BWExportSettings,
    BWExportItem,
)

def register():
    # 防止重复注册导致 already registered as a subclass 错误
    try:
        unregister()
    except Exception:
        pass
    # Properties & Preferences
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.bw_export = bpy.props.PointerProperty(type=BWExportSettings)
    # 仅在 bpy.data 有 scenes 属性时初始化，防止 _RestrictData 报错
    if hasattr(bpy.data, "scenes"):
        for scene in bpy.data.scenes:
            if not hasattr(scene, "bw_export") or scene.bw_export is None:
                scene.bw_export = bpy.context.scene.bw_export
    # 注册资源浏览器用的 CollectionProperty 和 IntProperty
    bpy.types.Scene.bw_export_list = bpy.props.CollectionProperty(type=BWExportItem)
    bpy.types.Scene.bw_export_index = bpy.props.IntProperty(name="Index", default=0)

    # UI
    register_ui()
    register_project_ui()
    register_model_ui()
    register_anim_ui()
    register_pack_ui()
    register_resources_ui()

    # Operators
    register_cli()
    register_project_ops()
    register_create_ops()
    register_export_model()
    register_export_anim()
    register_pack_textures()
    register_pack_assets()
    register_import_bw()

    # Workflows
    register_workflows()

def unregister():
    # Workflows
    unregister_workflows()

    # Operators
    unregister_import_bw()
    unregister_pack_assets()
    unregister_pack_textures()
    unregister_export_anim()
    unregister_export_model()
    unregister_create_ops()
    unregister_project_ops()
    unregister_cli()

    # UI
    unregister_resources_ui()
    unregister_pack_ui()
    unregister_anim_ui()
    unregister_model_ui()
    unregister_project_ui()
    unregister_ui()

    # Properties & Preferences
    try:
        del bpy.types.Scene.bw_export
    except Exception:
        pass
    try:
        del bpy.types.Scene.bw_export_list
    except Exception:
        pass
    try:
        del bpy.types.Scene.bw_export_index
    except Exception:
        pass
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass

if __name__ == "__main__":
    register()
