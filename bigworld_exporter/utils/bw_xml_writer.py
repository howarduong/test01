# bigworld_exporter/utils/bw_xml_writer.py
from mathutils import Vector
import os
import xml.etree.ElementTree as ET


def _indent(elem, level=0):
    # XML 缩进美化
    indent = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        for e in elem:
            _indent(e, level+1)
        if not e.tail or not e.tail.strip():
            e.tail = indent
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = indent

class ModelWriter:
    def __init__(self, root, name_tmpl):
        base = os.path.splitext(name_tmpl)[0]
        self.filepath = os.path.join(root, base + ".model")
        self.root = ET.Element("model")
        self.nodes = ET.SubElement(self.root, "nodes")

    def add_node(self, obj, coord_fn, parent):
        # 计算世界包围盒
        bbox = [coord_fn(obj.matrix_world @ Vector(c)) for c in obj.bound_box]
        mins = [min(v[i] for v in bbox) for i in range(3)]
        maxs = [max(v[i] for v in bbox) for i in range(3)]
        node = ET.SubElement(self.nodes, "node", name=obj.name,
                             parent=(parent.name if parent else ""))
        ET.SubElement(node, "bbox",
                      min="{} {} {}".format(*mins),
                      max="{} {} {}".format(*maxs))

    def save(self):
        _indent(self.root)
        tree = ET.ElementTree(self.root)
        tree.write(self.filepath, encoding="utf-8", xml_declaration=True)

class VisualWriter:
    def __init__(self, root, name_tmpl):
        base = os.path.splitext(name_tmpl)[0]
        self.xml_path = os.path.join(root, base + ".visual")
        # 二进制前缀，与 .bin 同名
        self.bin_prefix = os.path.join(root, base)
        self.root = ET.Element("visual")
        self.chunks_elem = ET.SubElement(self.root, "chunks")
        self.skel_elem = ET.SubElement(self.root, "skeletons")
        self.mats_elem = ET.SubElement(self.root, "materials")

    @property
    def bin_path(self):
        # .bin 文件路径
        return self.bin_prefix + ".bin"

    def add_chunk(self, obj_name, idx, mat_id):
        ET.SubElement(self.chunks_elem, "chunk",
                      object=obj_name,
                      id=str(idx),
                      material=str(mat_id))

    def add_skeleton(self, arm_name, bone_hierarchy, bind_matrices):
        sk = ET.SubElement(self.skel_elem, "skeleton", name=arm_name)
        for bone_name, parent in bone_hierarchy:
            ET.SubElement(sk, "bone", name=bone_name, parent=parent)
        # 可按需添加 bind pose 矩阵

    def add_material_ref(self, mat_name, mat_file):
        ET.SubElement(self.mats_elem, "material",
                      name=mat_name, file=mat_file)

    def save(self):
        _indent(self.root)
        tree = ET.ElementTree(self.root)
        tree.write(self.xml_path, encoding="utf-8", xml_declaration=True)

class PrimitiveWriter:
    def __init__(self, root, name_tmpl):
        base = os.path.splitext(name_tmpl)[0]
        self.filepath = os.path.join(root, base + ".primitives")
        self.root = ET.Element("primitives")

    def add(self, name, data: dict):
        # data 应包含 type, verts 或 min/max 等
        prim = ET.SubElement(self.root, "primitive",
                              name=name, type=data.get("type",""))
        if data["type"] == "box":
            ET.SubElement(prim, "min", value="{} {} {}".format(*data["min"]))
            ET.SubElement(prim, "max", value="{} {} {}".format(*data["max"]))
        elif data["type"] == "hull":
            for v in data["verts"]:
                ET.SubElement(prim, "vertex", value="{} {} {}".format(*v))
        # others 按需扩展

    def save(self):
        _indent(self.root)
        tree = ET.ElementTree(self.root)
        tree.write(self.filepath, encoding="utf-8", xml_declaration=True)

class AnimWriter:
    def __init__(self, root, arm_name, fps, start, end):
        self.xml_path = os.path.join(root, arm_name + ".animation")
        self.bin_path = os.path.join(root, arm_name + ".bin")
        self.root = ET.Element("animation", name=arm_name,
                               fps=str(fps),
                               start=str(start), end=str(end))
        self.bones_elem = ET.SubElement(self.root, "bones")

    def write_bone_frame(self, bone_name, matrix):
        bone = ET.SubElement(self.bones_elem, "frame", bone=bone_name)
        # matrix 为 4x4，写入行优先空格分隔
        flat = [str(v) for row in matrix for v in row]
        bone.text = " ".join(flat)

    def save(self):
        _indent(self.root)
        tree = ET.ElementTree(self.root)
        tree.write(self.xml_path, encoding="utf-8", xml_declaration=True)
