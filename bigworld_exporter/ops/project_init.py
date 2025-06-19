# bigworld_exporter/ops/project_init.py

import bpy, os
from bpy.types import Operator
from bpy.props import StringProperty
from ..utils.bw_logging import get_logger

logger = get_logger(__name__)

class BW_OT_project_wizard(Operator):
    bl_idname = "bw.project_wizard"
    bl_label = "Create BigWorld Project Structure"
    bl_description = "Generate standard folders for a new BigWorld project"
    bl_options = {'REGISTER', 'UNDO'}

    root: StringProperty(
        name="Project Root",
        description="Base directory for new project",
        subtype='DIR_PATH',
        default="//"
    )

    def execute(self, context):
        root = bpy.path.abspath(self.root)
        subdirs = ["models","visuals","primitives","animations","materials","textures","shaders","logs"]
        try:
            for sd in subdirs:
                path = os.path.join(root, sd)
                os.makedirs(path, exist_ok=True)
                logger.info(f"Created folder: {path}")
            context.scene.bw_export.resource_root = root
            self.report({'INFO'}, f"Project structure created under {root}")
            return {'FINISHED'}
        except Exception as e:
            logger.error(f"Project wizard error: {e}", exc_info=True)
            self.report({'ERROR'}, f"Failed to create project folders: {e}")
            return {'CANCELLED'}

    def invoke(self, context, event):
        self.root = context.scene.bw_export.resource_root
        return context.window_manager.invoke_props_dialog(self)

def register_project_ops():
    bpy.utils.register_class(BW_OT_project_wizard)

def unregister_project_ops():
    bpy.utils.unregister_class(BW_OT_project_wizard)
