# bigworld_exporter/utils/bw_pipeline_hooks.py

import os
import subprocess
import sys
from .bw_logging import get_logger

logger = get_logger(__name__)

def _run_script(python_exe, script_path, args):
    """
    调用外部 Python 脚本
    """
    cmd = [python_exe or sys.executable, script_path] + args
    logger.info("Running: " + " ".join(cmd))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate()
    if out:
        logger.info(out.strip())
    if err:
        logger.error(err.strip())
    if proc.returncode != 0:
        raise RuntimeError(f"Script {script_path} exited with {proc.returncode}")

def run_all(
    root: str,
    convert_model_script: str,
    convert_materials_script: str,
    texture_tool_exe: str,
    package_builder_script: str,
    chunk_viz_script: str,
    resource_scanner_script: str,
    enable_vcs_hook: bool = False
):
    """
    串联调用：convertModel → convertMaterials → chunkViz → packageBuilder → resourceScanner → VCS Hook
    """
    # 1) convertModel.py
    if convert_model_script and os.path.isfile(convert_model_script):
        _run_script(None, convert_model_script, ['--input', root])
    else:
        logger.warning("convertModel.py not configured or not found")

    # 2) convertMaterials.py
    if convert_materials_script and os.path.isfile(convert_materials_script):
        _run_script(None, convert_materials_script, ['--input', root])
    else:
        logger.warning("convertMaterials.py not configured or not found")

    # 3) chunkViz.py
    if chunk_viz_script and os.path.isfile(chunk_viz_script):
        _run_script(None, chunk_viz_script, ['--input', root, '--output', os.path.join(root, 'chunk_viz.png')])
    else:
        logger.info("chunkViz.py skipped")

    # 4) packageBuilder.py
    if package_builder_script and os.path.isfile(package_builder_script):
        _run_script(None, package_builder_script, ['--root', root])
    else:
        logger.warning("packageBuilder.py not configured or not found")

    # 5) resourceScanner.py
    if resource_scanner_script and os.path.isfile(resource_scanner_script):
        _run_script(None, resource_scanner_script, ['--root', root, '--report', os.path.join(root, 'resource_report.txt')])
    else:
        logger.info("resourceScanner.py skipped")

    # 6) VCS Hook 生成
    if enable_vcs_hook:
        try:
            from .ci_cd_hooks import install_hooks
            install_hooks(root)
        except Exception as e:
            logger.error(f"VCS hook install failed: {e}")
