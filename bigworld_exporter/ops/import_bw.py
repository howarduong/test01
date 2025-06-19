# bigworld_exporter/ops/import_bw.py

import os
import bpy
import xml.etree.ElementTree as ET
from mathutils import Vector
from bpy.types import Operator
from bpy.props import StringProperty
from ..utils.bw_logging import get_logger

logger = get_logger(__name__)

class BW_OT_import_bw(Operator):
    bl_idname = "bw.import_bw"
    bl_label = "Import BigWorld Asset"
    bl_description = "Import .model, .visual, .primitives into Blender"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: StringProperty(
        name="File Path",
        description="Path to .model/.visual/.primitives file",
        subtype='FILE_PATH'
    )
    filter_glob: StringProperty(
        default="*.model;*.visual;*.primitives",
        options={'HIDDEN'}
    )

    def execute(self, context):
        ext = os.path.splitext(self.filepath)[1].lower()
        try:
            if ext == '.model':
                self._import_model(context)
            elif ext == '.visual':
                self._import_visual(context)
            elif ext == '.primitives':
                self._import_primitives(context)
            else:
                self.report({'ERROR'}, f"Unsupported format: {ext}")
                return {'CANCELLED'}
            return {'FINISHED'}
        except Exception as e:
            logger.error("Import failed", exc_info=True)
            self.report({'ERROR'}, f"Import failed: {e}")
            return {'CANCELLED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def _import_model(self, context):
        # 解析 .model，创建空对象并设置位置于 bbox 中心
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        nodes = root.find('nodes')
        for node in nodes.findall('node'):
            name = node.get('name')
            bbox = node.find('bbox')
            if bbox is not None:
                min_vals = list(map(float, bbox.get('min').split()))
                max_vals = list(map(float, bbox.get('max').split()))
                center = [(mi+ma)/2 for mi,ma in zip(min_vals, max_vals)]
            else:
                center = (0,0,0)
            empty = bpy.data.objects.new(name, None)
            empty.location = Vector(center)
            context.collection.objects.link(empty)
        self.report({'INFO'}, f"Imported {len(nodes)} nodes from .model")

    def _import_visual(self, context):
        # 这里只做占位：创建空 Mesh，实际顶点/索引重建留待后续完善
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        chunks = root.find('chunks')
        mesh = bpy.data.meshes.new("ImportedVisual")
        obj = bpy.data.objects.new("VisualMesh", mesh)
        context.collection.objects.link(obj)
        # 后续可解析二进制，重建 Mesh 数据
        self.report({'INFO'}, f"Found {len(chunks)} chunks; mesh created as placeholder")

    def _import_primitives(self, context):
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        count = 0
        for prim in root.findall('primitive'):
            name = prim.get('name')
            # 仅创建 empty 来标记
            empty = bpy.data.objects.new(name, None)
            context.collection.objects.link(empty)
            count += 1
        self.report({'INFO'}, f"Imported {count} primitives as empties")

def register_import_bw():
    bpy.utils.register_class(BW_OT_import_bw)

def unregister_import_bw():
    bpy.utils.unregister_class(BW_OT_import_bw)
