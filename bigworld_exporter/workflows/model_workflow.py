# bigworld_exporter/workflows/model_workflow.py

import bpy

def run_model_workflow(scan_after=True):
    """
    模型导出完整流程：
      1) 导出 .model/.visual/.primitives
      2) 可选：资源依赖扫描
    """
    bpy.ops.bw.export_model()
    if scan_after:
        bpy.ops.bw.resource_scan()
