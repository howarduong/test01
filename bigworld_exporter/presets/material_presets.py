# bigworld_exporter/presets/material_presets.py

import bpy

def create_bw_surface_material(name="BW_Surface"):
    """
    快速新建一个 BigWorld 官方表面材质模板：
    - Principled BSDF 节点为主
    - 可在 Properties 界面一键实例化
    """
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    # 创建输出节点
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    out.location = (400, 0)
    # 创建 Principled
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    # 连接
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    # 默认贴图插槽、颜色参数留白
    return mat

def register_material_presets():
    # 可以在这里注册菜单或快捷操作
    pass

def unregister_material_presets():
    pass
