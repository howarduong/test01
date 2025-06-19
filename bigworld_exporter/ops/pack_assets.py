# bigworld_exporter/ops/pack_assets.py

import bpy
from bpy.types import Operator
from ..properties import BWExportSettings
from ..utils import bw_pipeline_hooks, bw_logging

logger = bw_logging.get_logger()

class BW_OT_pack_assets(Operator):
    bl_idname = "bw.pack_assets"
    bl_label = "Run Full Pipeline"
    bl_description = "Run convertModel, convertMaterials, chunkViz, packageBuilder, resourceScanner"
    bl_options = {'REGISTER'}

    def execute(self, context):
        s: BWExportSettings = context.scene.bw_export
        prefs = context.preferences.addons["bigworld_exporter"].preferences
        root = bpy.path.abspath(s.resource_root)
        try:
            logger.info("Running full pipeline...")
            bw_pipeline_hooks.run_all(
                root,
                prefs.convert_model_script,
                prefs.convert_materials_script,
                prefs.texture_tool_executable,
                prefs.package_builder_script,
                prefs.chunk_viz_script,
                prefs.resource_scanner_script,
                prefs.enable_vcs_hook
            )
            self.report({'INFO'}, "Full pipeline complete")
            return {'FINISHED'}
        except Exception as e:
            logger.error("Pipeline failed", exc_info=True)
            self.report({'ERROR'}, f"Pipeline failed: {e}")
            return {'CANCELLED'}

def register_pack_assets():
    bpy.utils.register_class(BW_OT_pack_assets)

def unregister_pack_assets():
    bpy.utils.unregister_class(BW_OT_pack_assets)
