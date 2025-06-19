# bigworld_exporter/ops/batch_cli.py

import bpy
import sys
from bpy.types import Operator
from bpy.props import StringProperty
from ..ops.export_model import BW_OT_export_model
from ..ops.export_anim import BW_OT_export_anim
from ..ops.pack_assets import BW_OT_pack_assets
from ..ops.resource_scan import BW_OT_resource_scan
from ..ops.import_bw import BW_OT_import_bw

class BW_OT_batch_cli(Operator):
    bl_idname = "bw.batch_cli"
    bl_label = "BigWorld Batch CLI"
    bl_description = "Run batch operations via CLI arguments"
    bl_options = {'INTERNAL'}

    args: StringProperty(
        name="CLI Args",
        description="Space-separated CLI flags"
    )

    def execute(self, context):
        argv = self.args.split()
        # Model export
        if '--export-model' in argv:
            bpy.ops.bw.export_model()
        # Animation export
        if '--export-anim' in argv:
            bpy.ops.bw.export_anim()
        # Full pipeline (pack_assets)
        if '--pack-all' in argv or '--pipeline' in argv:
            bpy.ops.bw.pack_assets()
        # Resource scan
        if '--scan' in argv:
            bpy.ops.bw.resource_scan()
        # Import
        if '--import' in argv:
            # Expect next arg is filepath
            try:
                idx = argv.index('--import')
                path = argv[idx+1]
                bpy.ops.bw.import_bw(filepath=path)
            except:
                self.report({'ERROR'}, "Usage: --import <filepath>")
                return {'CANCELLED'}
        return {'FINISHED'}

def register_cli():
    bpy.utils.register_class(BW_OT_batch_cli)

def unregister_cli():
    bpy.utils.unregister_class(BW_OT_batch_cli)
