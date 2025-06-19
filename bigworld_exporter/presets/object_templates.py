# bigworld_exporter/presets/object_templates.py

import bpy
from mathutils import Vector
import bmesh

def create_collision_template(name="BW_Collision", prim_type='BOX'):
    """
    返回一个新生成的空物体或网格，供后续贴 Scene 中。
    prim_type: 'BOX','CAPSULE','HULL'
    """
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    bm = bmesh.new()
    # 根据类型建模
    if prim_type=='BOX':
        bmesh.ops.create_cube(bm, size=1.0)
    elif prim_type=='CAPSULE':
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                              segments=16, diameter1=1.0, diameter2=1.0, depth=1.0)
    else:  # HULL
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.convex_hull(bm, input=bm.verts)
    bm.to_mesh(mesh); bm.free()
    # 标记
    obj["bw_collision"] = prim_type
    return obj

def register_object_templates():
    pass

def unregister_object_templates():
    pass
