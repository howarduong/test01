# bigworld_exporter/workflows/anim_workflow.py

import bpy

def run_anim_workflow(scan_after=True):
    """
    动画导出完整流程：
      1) 导出 .animation/.bin (+Morph)
      2) 可选：资源依赖扫描
    """
    bpy.ops.bw.export_anim()
    if scan_after:
        bpy.ops.bw.resource_scan()
