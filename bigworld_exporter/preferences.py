# bigworld_exporter/preferences.py

import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty, BoolProperty

class BigWorldExporterPreferences(AddonPreferences):
    # 这里一定要写成插件文件夹名，不要用 __package__ 动态获取
    bl_idname = "bigworld_exporter"

    # BigWorld Python 后处理脚本
    convert_model_script: StringProperty(
        name="Convert Model Script",
        description="Path to BigWorld convertModel.py",
        subtype='FILE_PATH',
        default=""
    )
    convert_materials_script: StringProperty(
        name="Convert Materials Script",
        description="Path to BigWorld convertMaterials.py",
        subtype='FILE_PATH',
        default=""
    )
    texture_tool_executable: StringProperty(
        name="Texture Tool Executable",
        description="Path to external texture compression tool (e.g. NVCompress)",
        subtype='FILE_PATH',
        default=""
    )
    package_builder_script: StringProperty(
        name="Package Builder Script",
        description="Path to BigWorld packageBuilder.py",
        subtype='FILE_PATH',
        default=""
    )
    chunk_viz_script: StringProperty(
        name="ChunkViz Script",
        description="Path to BigWorld chunkViz.py (optional)",
        subtype='FILE_PATH',
        default=""
    )
    resource_scanner_script: StringProperty(
        name="ResourceScanner Script",
        description="Path to BigWorld resourceScanner.py (optional)",
        subtype='FILE_PATH',
        default=""
    )
    enable_vcs_hook: BoolProperty(
        name="Enable VCS Hook Generation",
        description="Generate Git/Perforce/SVN hooks after export",
        default=False
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="BigWorld External Tools Paths", icon='PREFERENCES')
        box = layout.box()
        box.prop(self, "convert_model_script")
        box.prop(self, "convert_materials_script")
        box.prop(self, "texture_tool_executable")
        box.prop(self, "package_builder_script")
        box.prop(self, "chunk_viz_script")
        box.prop(self, "resource_scanner_script")
        layout.prop(self, "enable_vcs_hook")

# no extra code beyond class definition!
