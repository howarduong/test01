# bigworld_exporter/utils/ci_cd_hooks.py

import os
import shutil
from .bw_logging import get_logger

logger = get_logger(__name__)

HOOK_TEMPLATES_DIR = os.path.join(
    os.path.dirname(__file__), os.pardir, "presets", "hooks"
)

def install_hooks(project_root: str):
    """
    根据项目类型（Git / Perforce）将预置的 BigWorld 钩子脚本拷贝到相应目录。
    presumes:
      presets/hooks/git/post-commit
      presets/hooks/perforce/trigger.p4s
    """
    # Git 钩子
    git_hooks_dir = os.path.join(project_root, ".git", "hooks")
    if os.path.isdir(git_hooks_dir):
        src = os.path.join(HOOK_TEMPLATES_DIR, "git", "post-commit")
        dst = os.path.join(git_hooks_dir, "post-commit")
        try:
            shutil.copyfile(src, dst)
            os.chmod(dst, 0o755)
            logger.info(f"Installed Git hook: {dst}")
        except Exception as e:
            logger.error(f"Failed to install Git hook: {e}")
    else:
        logger.info("No .git/hooks found, skipping Git hook installation")

    # Perforce 钩子
    p4_hooks_dir = os.path.join(project_root, "p4_triggers")
    if os.path.isdir(HOOK_TEMPLATES_DIR + "/perforce"):
        os.makedirs(p4_hooks_dir, exist_ok=True)
        src = os.path.join(HOOK_TEMPLATES_DIR, "perforce", "trigger.p4s")
        dst = os.path.join(p4_hooks_dir, "trigger.p4s")
        try:
            shutil.copyfile(src, dst)
            logger.info(f"Installed Perforce trigger: {dst}")
            logger.info("Remember to configure your Perforce server to use this trigger")
        except Exception as e:
            logger.error(f"Failed to install Perforce trigger: {e}")
    else:
        logger.info("No Perforce hook template found, skipping Perforce hook installation")
