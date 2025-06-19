# bigworld_exporter/utils/bw_material_map.py

import os
import xml.etree.ElementTree as ET
from mathutils import Color
import bpy

# 简单映射：Blender Principled BSDF → BigWorld bw_surface
SHADER_MAP = {
    'BSDF_PRINCIPLED': 'bw_surface',
    # 可扩展：其他自定义节点
}

def export(mat: bpy.types.Material, root: str):
    """
    将 Blender Material 导出为 BigWorld .material 文件。
    文件保存在 root/materials/<mat.name>.material
    """
    # 确保输出目录
    out_dir = os.path.join(root, "materials")
    os.makedirs(out_dir, exist_ok=True)
    # 创建根节点
    m_root = ET.Element("material", name=mat.name)
    # 默认 shader
    shader = None
    # 在节点树中寻找 Principled BSDF
    if mat.use_nodes and mat.node_tree:
        for node in mat.node_tree.nodes:
            if node.type in SHADER_MAP:
                shader = SHADER_MAP[node.type]
                break
    if shader is None:
        shader = mat.get("bw_shader", "bw_surface")
    m_root.set("shader", shader)

    # 参数 & 贴图
    if mat.use_nodes and mat.node_tree:
        for node in mat.node_tree.nodes:
            # 处理 Base Color
            if node.type == 'BSDF_PRINCIPLED':
                rgb = node.inputs['Base Color'].default_value[:3]
                col = Color(rgb).hsv  # 仅示例，可直接使用 rgb
                ET.SubElement(m_root, "param", name="diffuseColor",
                              value=f"{rgb[0]} {rgb[1]} {rgb[2]}")
                # 贴图
                links = node.inputs['Base Color'].links
                if links:
                    src = links[0].from_node
                    if src.type == 'TEX_IMAGE' and src.image:
                        img_path = bpy.path.abspath(src.image.filepath)
                        rel = os.path.relpath(img_path, root)
                        ET.SubElement(m_root, "texture",
                                      slot="diffuse", file=rel)
                # 其他参数可按需添加：Specular, Roughness, Normal Map...
    else:
        # 非节点材质：使用 diffuse_color
        rgb = mat.diffuse_color[:3]
        ET.SubElement(m_root, "param", name="diffuseColor",
                      value=f"{rgb[0]} {rgb[1]} {rgb[2]}")

    # 写出
    tree = ET.ElementTree(m_root)
    out_file = os.path.join(out_dir, f"{mat.name}.material")
    tree.write(out_file, encoding="utf-8", xml_declaration=True)
    return out_file
