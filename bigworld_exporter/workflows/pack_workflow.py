# bigworld_exporter/workflows/pack_workflow.py

import bpy

def run_pack_workflow():
    """
    打包 & 后处理完整流程：
      1) 贴图打包
      2) Pipeline（convertModel, materials, chunkViz, packageBuilder, resourceScanner, VCS hook）
    """
    bpy.ops.bw.pack_textures()
    bpy.ops.bw.pack_assets()
