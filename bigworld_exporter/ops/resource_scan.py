# bigworld_exporter/ops/resource_scan.py

import os
import bpy
from bpy.types import Operator
from bpy.props import BoolProperty
from ..utils.bw_pipeline_hooks import _run_script
from ..preferences import BigWorldExporterPreferences
from ..utils.bw_logging import get_logger

logger = get_logger(__name__)

class BW_OT_resource_scan(Operator):
    bl_idname = "bw.resource_scan"
    bl_label = "Resource Dependency Scan"
    bl_description = "Scan BigWorld asset files for missing resource dependencies"
    bl_options = {'REGISTER'}

    report_to_console: BoolProperty(
        name="Verbose",
        default=False,
        description="Print missing dependencies to console"
    )

    def execute(self, context):
        prefs: BigWorldExporterPreferences = context.preferences.addons["bigworld_exporter"].preferences
        script = prefs.resource_scanner_script
        root = bpy.path.abspath(context.scene.bw_export.resource_root)
        if not script or not os.path.isfile(script):
            self.report({'ERROR'}, "resourceScanner.py path not configured or invalid")
            return {'CANCELLED'}
        try:
            args = ['--root', root, '--report', os.path.join(root, 'resource_report.txt')]
            if self.report_to_console:
                args.append('--verbose')
            _run_script(None, script, args)
            self.report({'INFO'}, "Resource scan complete; see resource_report.txt")
            return {'FINISHED'}
        except Exception as e:
            logger.error("Resource scan failed", exc_info=True)
            self.report({'ERROR'}, f"Resource scan failed: {e}")
            return {'CANCELLED'}

def register_resource_scan():
    bpy.utils.register_class(BW_OT_resource_scan)

def unregister_resource_scan():
    bpy.utils.unregister_class(BW_OT_resource_scan)
