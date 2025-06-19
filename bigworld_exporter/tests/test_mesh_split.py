# bigworld_exporter/tests/test_mesh_split.py

import bpy
import bmesh
import pytest
from bigworld_exporter.utils.bw_mesh_split import split_mesh

@pytest.fixture
def simple_mesh_object(tmp_path):
    # 创建一个简单三角网格对象
    mesh = bpy.data.meshes.new("TestMesh")
    obj = bpy.data.objects.new("TestObj", mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(mesh); bm.free()
    return obj

def test_split_mesh_single_chunk(simple_mesh_object):
    obj = simple_mesh_object
    # 阈值足够大，只生成一个 chunk
    chunks = split_mesh(obj, max_verts=1000, max_indices=1000, grouping='OBJ')
    assert len(chunks) == 1
    chunk = chunks[0]
    # 顶点数为8，索引数为36（12三角形×3）
    assert len(chunk.vertices) == 8
    assert len(chunk.indices) == 36

def test_split_mesh_multiple_chunks(simple_mesh_object):
    obj = simple_mesh_object
    # 设置极低阈值，强制切多块
    chunks = split_mesh(obj, max_verts=4, max_indices=6, grouping='OBJ')
    assert len(chunks) > 1
    # 所有 chunk 顶点总数和索引总数与原始保持一致
    total_verts = sum(len(c.vertices) for c in chunks)
    total_inds = sum(len(c.indices) for c in chunks)
    assert total_verts >= 8
    assert total_inds >= 36
