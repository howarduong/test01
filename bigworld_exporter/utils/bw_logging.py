# bigworld_exporter/utils/bw_logging.py

import os, logging
import bpy

LOG_DIR = bpy.utils.user_resource('SCRIPTS', path="bigworld_exporter/logs", create=True)
LOG_FILE = os.path.join(LOG_DIR, "exporter.log")

def _ensure_log_dir():
    os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name=__name__):
    """
    获取全局 logger。日志会同时输出到控制台和用户目录下的 exporter.log。
    """
    _ensure_log_dir()
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # 已初始化
    logger.setLevel(logging.DEBUG)
    # File handler
    fh = logging.FileHandler(LOG_FILE, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # Formatter
    fmt = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s')
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
