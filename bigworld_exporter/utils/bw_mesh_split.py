# bigworld_exporter/utils/bw_mesh_split.py

import bmesh
from mathutils import Vector
from collections import defaultdict

class Chunk:
    def __init__(self, mat_id):
        self.mat_id = mat_id
        self.vertices = []   # list of Vector
        self.indices = []    # list of ints

def split_mesh(obj, max_verts, max_indices, grouping='MAT'):
    """
    将 obj.data 切分成多个 chunk，每个 chunk 顶点 ≤ max_verts, 索引 ≤ max_indices。
    grouping: 'MAT'（按材质）、'OBJ'（按对象整体）、'UG'（按自定义组属性）
    返回 List[Chunk]
    """
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()

    # 按分组策略收集 face 列表
    if grouping == 'MAT':
        groups = defaultdict(list)
        for f in bm.faces:
            mat_id = me.polygons[f.index].material_index
            groups[mat_id].append(f)
    elif grouping == 'OBJ':
        groups = {0: list(bm.faces)}  # 全部归为一组
    else:  # 用户组：依赖 obj["bw_group"] 属性划分
        groups = defaultdict(list)
        for f in bm.faces:
            gid = f[bw_group] if hasattr(f, 'bw_group') else 0
            groups[gid].append(f)

    chunks = []
    for mat_id, faces in groups.items():
        cur = Chunk(mat_id)
        vert_map = {}
        for f in faces:
            loop_idxs = []
            for lv in f.verts:
                orig_idx = lv.index
                if orig_idx not in vert_map:
                    vert_map[orig_idx] = len(cur.vertices)
                    co = obj.matrix_world @ lv.co
                    cur.vertices.append(co)
                loop_idxs.append(vert_map[orig_idx])
            # 三角化：若多边形，把 face.loops → 三角扇
            if len(loop_idxs) == 3:
                cur.indices.extend(loop_idxs)
            else:
                for i in range(1, len(loop_idxs)-1):
                    cur.indices.extend([loop_idxs[0], loop_idxs[i], loop_idxs[i+1]])
            # 检查阈值
            if len(cur.vertices) >= max_verts or len(cur.indices) >= max_indices:
                chunks.append(cur)
                cur = Chunk(mat_id)
                vert_map = {}
        if cur.vertices:
            chunks.append(cur)

    bm.free()
    return chunks
