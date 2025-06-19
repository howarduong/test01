# bigworld_exporter/tests/test_xml_writer.py

import os
import tempfile
import xml.etree.ElementTree as ET
import pytest
from bigworld_exporter.utils.bw_xml_writer import ModelWriter, VisualWriter, PrimitiveWriter, AnimWriter

@pytest.fixture
def temp_dir(tmp_path):
    return str(tmp_path)

def test_model_writer(temp_dir):
    mw = ModelWriter(temp_dir, "scene_test.model")
    # 模拟添加节点
    class Dummy:
        def __init__(self, name, bbox):
            self.name = name
            self.bound_box = bbox
            self.parent = None
            self.matrix_world = [[1,0,0,0],[0,1,0,0],[0,0,1,0]]
    # Dummy.bound_box: 8个顶点
    bbox = [(x,y,z) for x in (0,1) for y in (0,1) for z in (0,1)]
    d = Dummy("Node1", bbox)
    mw.add_node(d, lambda v: v, None)
    mw.save()
    path = os.path.join(temp_dir, "scene_test.model")
    assert os.path.isfile(path)
    # 验证根节点与子节点
    tree = ET.parse(path)
    root = tree.getroot()
    assert root.tag == "model"
    nodes = root.find("nodes")
    assert nodes.find("node").attrib["name"] == "Node1"

def test_visual_writer_and_primitive_and_anim(temp_dir):
    vw = VisualWriter(temp_dir, "vis_test.visual")
    vw.add_chunk("Obj", 0, 2)
    vw.add_material_ref("Mat1", "Mat1.material")
    vw.save()
    vpath = os.path.join(temp_dir, "vis_test.visual")
    assert os.path.isfile(vpath)
    tree = ET.parse(vpath)
    assert tree.getroot().find("chunks").find("chunk").attrib["material"] == "2"

    pw = PrimitiveWriter(temp_dir, "prim_test.primitives")
    data = {"type":"box", "min":(0,0,0), "max":(1,1,1)}
    pw.add("P", data)
    pw.save()
    ppath = os.path.join(temp_dir, "prim_test.primitives")
    assert os.path.isfile(ppath)
    root = ET.parse(ppath).getroot()
    assert root.find("primitive").attrib["type"] == "box"

    aw = AnimWriter(temp_dir, "arm", 24, 1, 2)
    # 构造4x4矩阵
    import mathutils
    mat = mathutils.Matrix.Identity(4)
    aw.write_bone_frame("B", mat)
    aw.save()
    apath = os.path.join(temp_dir, "arm.animation")
    assert os.path.isfile(apath)
    root = ET.parse(apath).getroot()
    assert root.attrib["fps"] == "24"
