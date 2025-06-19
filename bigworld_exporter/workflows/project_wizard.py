# bigworld_exporter/workflows/project_wizard.py

import bpy

def run_project_wizard():
    """
    封装调用：新建项目结构向导
    """
    bpy.ops.bw.project_wizard('INVOKE_DEFAULT')
