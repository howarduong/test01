# bigworld_exporter/utils/bw_morph.py

import os
import bpy
from .bw_logging import get_logger

logger = get_logger(__name__)

def export(obj: bpy.types.Object, start: int, end: int, root: str):
    """
    导出 Shape Key Morph targets。
    会在 root/<obj.name>_morphs/ 下生成 .bin + .animation xml 列表
    """
    sk = obj.data.shape_keys
    if not sk:
        return
    base = sk.key_blocks[0]
    out_dir = os.path.join(root, f"{obj.name}_morphs")
    os.makedirs(out_dir, exist_ok=True)

    for key in sk.key_blocks[1:]:
        count = end - start + 1
        bin_path = os.path.join(out_dir, f"{key.name}.bin")
        xml_path = os.path.join(out_dir, f"{key.name}.animation")
        # Binary: 每帧每顶点偏移 (dx, dy, dz)
        with open(bin_path, "wb") as fp:
            for f in range(start, end+1):
                key.value = (f-start)/(count-1)
                bpy.context.view_layer.update()
                for v in obj.data.vertices:
                    delta = v.co - base.data[v.index].co
                    fp.write(struct.pack("<3f", delta.x, delta.y, delta.z))
        # XML: minimal descriptor
        with open(xml_path, "w", encoding="utf-8") as xf:
            xf.write(f'<morph name="{key.name}" frames="{count}" />\n')
        logger.info(f"Exported morph: {key.name} for {obj.name}")
