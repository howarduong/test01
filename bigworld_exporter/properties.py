# bigworld_exporter/properties.py

import bpy
import os

def update_resource_list(self, context):
    """更新资源列表：读取 resource_root 目录下所有文件，并添加到 Scene 的 bw_export_list 中"""
    scene = context.scene
    root = bpy.path.abspath(self.resource_root)
    # 清空现有列表
    scene.bw_export_list.clear()
    if not os.path.isdir(root):
        print("资源根目录无效:", root)
        return
    files = sorted(os.listdir(root))
    for f in files:
        item = scene.bw_export_list.add()
        item.filepath = f
    print("更新资源列表:", files)


from bpy.types import PropertyGroup
from bpy.props import (
    StringProperty, IntProperty, EnumProperty, BoolProperty,
    CollectionProperty
)

class BWExportSettings(PropertyGroup):
    resource_root: StringProperty(
        name="Resource Root",
        subtype='DIR_PATH',
        default="//export/",
        description="Base folder for all BigWorld exports",
        update=update_resource_list
    )

    model_name: StringProperty(
        name="Model File",
        default="{scene}.model",
        description="Template for .model filename, supports {scene} and {object}"
    )
    up_axis: EnumProperty(
        name="Up Axis",
        items=[
            ('Z', 'Z Up', 'Z轴朝上'),
            ('Y', 'Y Up', 'Y轴朝上')
        ],
        default='Z',
        description="Choose world up axis for BigWorld"
    )
    max_verts: IntProperty(
        name="Max Verts/Chunk",
        default=60000, min=1,
        description="Maximum vertices per chunk"
    )
    max_indices: IntProperty(
        name="Max Indices/Chunk",
        default=180000, min=1,
        description="Maximum indices per chunk"
    )
    grouping: EnumProperty(
        name="Grouping Mode",
        items=[
            ('MAT', 'Material', '按材质分组'),
            ('OBJ', 'Object', '按对象分组'),
            ('UG', 'User Group', '按用户分组')
        ],
        default='MAT',
        description="How to group faces into chunks"
    )
    include_normals: BoolProperty(
        name="Normals",
        default=True
    )
    include_tangents: BoolProperty(
        name="Tangents",
        default=False
    )
    include_uvs: BoolProperty(
        name="UV Channels",
        default=True
    )
    include_vcolor: BoolProperty(
        name="Vertex Colors",
        default=False
    )
    include_skin: BoolProperty(
        name="Skin Weights",
        default=True
    )
    export_primitives: BoolProperty(
        name="Export Primitives",
        default=False
    )
    collision_type: EnumProperty(
        name="Collision Type",
        items=[
            ('NONE', 'None', '无碰撞体'),
            ('BOX', 'Box', '盒状碰撞体'),
            ('CAPSULE', 'Capsule', '胶囊体碰撞体'),
            ('HULL', 'Convex Hull', '凸包碰撞体')
        ],
        default='NONE'
    )
    collision_filter: StringProperty(
        name="Collision Filter",
        default="*",
        description="Object name or property filter for exporting primitives"
    )
    export_materials: BoolProperty(
        name="Export .material",
        default=False
    )
    tex_compress: BoolProperty(
        name="Texture Compression",
        default=False
    )
    md5: BoolProperty(
        name="Generate MD5",
        default=False
    )
    post_tools: BoolProperty(
        name="Run Post-Tools",
        default=False
    )
    # Animation
    anim_fps: IntProperty(
        name="Anim FPS",
        default=30, min=1
    )
    anim_range: EnumProperty(
        name="Frame Range",
        items=[('SCENE', 'Scene', '场景范围'), ('CUSTOM', 'Custom', '自定义范围')],
        default='SCENE'
    )
    custom_start: IntProperty(
        name="Start Frame", default=1
    )
    custom_end: IntProperty(
        name="End Frame", default=250
    )
    morphs: BoolProperty(
        name="Export Morphs",
        default=False
    )
    # LOD
    lod_mode = EnumProperty(
        name="LOD Mode",
        items=[('MANUAL','Manual'),('AUTO','Auto-Decimate')],
        default='MANUAL'
    )
    lod_ratios = CollectionProperty(
        name="LOD Ratios",
        type=PropertyGroup
    )
    # CLI
    cli_args: StringProperty(
        name="CLI Args",
        default="",
        description="Command-line arguments for batch mode"
    )
class BWExportItem(PropertyGroup):
    filepath: StringProperty(name="File Path")
