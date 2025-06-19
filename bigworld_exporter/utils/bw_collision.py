# bigworld_exporter/utils/bw_collision.py

import os
import bmesh
import bpy
from mathutils import Vector
from .bw_logging import get_logger

logger = get_logger(__name__)

def generate(obj: bpy.types.Object, up_axis='Z'):
    """
    根据 obj["bw_collision"] 属性和 up_axis，返回 dict:
      {'type': 'box'|'capsule'|'hull', 'min':(), 'max':(), 'verts':[...] }
    """
    ctype = obj.get("bw_collision", "BOX").lower()
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()
    # World-space verts
    world_verts = [obj.matrix_world @ v.co for v in bm.verts]

    data = {'type': ctype}
    if ctype == 'box':
        # 计算轴对齐包围盒
        xs = [v.x for v in world_verts]; ys = [v.y for v in world_verts]; zs = [v.z for v in world_verts]
        data['min'] = (min(xs), min(ys), min(zs))
        data['max'] = (max(xs), max(ys), max(zs))
    elif ctype == 'hull':
        # 简单凸包
        hull = bmesh.ops.convex_hull(bm, input=bm.verts)
        hull_verts = [obj.matrix_world @ v.co for v in hull.get('geom', []) if hasattr(v, 'co')]
        data['verts'] = [(v.x, v.y, v.z) for v in hull_verts]
    elif ctype == 'capsule':
        # 近似：取 Y 轴为高度，X,Z 作为半径
        xs = [v.x for v in world_verts]; zs = [v.z for v in world_verts]
        ys = [v.y for v in world_verts]
        r = max(max(xs)-min(xs), max(zs)-min(zs)) / 2
        height = max(ys)-min(ys)
        center = Vector(((min(xs)+max(xs))/2, (min(ys)+max(ys))/2, (min(zs)+max(zs))/2))
        data['radius'] = r
        data['height'] = height
        data['center'] = (center.x, center.y, center.z)
    else:
        logger.warning(f"Unknown collision type: {ctype}, default to box")
        return generate(obj, 'box')

    bm.free()
    return data
