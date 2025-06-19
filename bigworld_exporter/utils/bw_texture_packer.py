# bigworld_exporter/utils/bw_texture_packer.py

import os, shutil
import subprocess
try:
    from PIL import Image
except ImportError:
    Image = None
from .bw_logging import get_logger

logger = get_logger(__name__)

def pack(root: str, compress: bool = False):
    """
    扫描 root/textures 目录下所有图片，
    用 Pillow 生成 Atlas 并保存到 root/textures/atlas.png，
    然后可选调用外部工具压缩成 DDS/ASTC 等。
    """
    tex_dir = os.path.join(root, "textures")
    if not os.path.isdir(tex_dir):
        logger.warning(f"No textures folder at {tex_dir}")
        return

    # 收集所有图像路径
    imgs = [os.path.join(tex_dir, f)
            for f in os.listdir(tex_dir)
            if f.lower().endswith((".png", ".jpg", ".tga"))]

    if not imgs:
        logger.info("No textures to pack")
        return

    # 简单水平拼接示例（如需复杂布局可按需改造）
    if Image:
        # 用 Pillow 拼接 Atlas
        images = [Image.open(p) for p in imgs]
        widths, heights = zip(*(i.size for i in images))
        total_w = sum(widths)
        max_h = max(heights)
        atlas = Image.new('RGBA', (total_w, max_h))
        x_offset = 0
        for img in images:
            atlas.paste(img, (x_offset, 0))
            x_offset += img.size[0]

        atlas_path = os.path.join(tex_dir, "atlas.png")
        atlas.save(atlas_path)
        logger.info(f"Atlas saved: {atlas_path}")
    else:
        logger.warning("Pillow not installed; skipping Atlas generation.")
        atlas_path = None
    widths, heights = zip(*(i.size for i in images))
    total_w = sum(widths)
    max_h = max(heights)
    atlas = Image.new('RGBA', (total_w, max_h))
    x_offset = 0
    for img in images:
        atlas.paste(img, (x_offset, 0))
        x_offset += img.size[0]

    atlas_path = os.path.join(tex_dir, "atlas.png")
    atlas.save(atlas_path)
    logger.info(f"Atlas saved: {atlas_path}")

    # 压缩：调用外部工具（如 NVCompress）
    if compress:
        # 如果 Atlas 可用则压缩它，否则尝试压缩原 textures 下所有图
        target = atlas_path if atlas_path else tex_dir
        exe = shutil.which("NVCompress") or shutil.which("textureTool")  # 兼容多种命令名
        if not exe:
            logger.error("NVCompress not found in PATH")
        else:
            if atlas_path:
                out = atlas_path.replace(".png", ".dds")
                cmd = [exe, "-nomipmap", atlas_path, out]
            else:
                # 把所有贴图逐个压缩
                cmd = [exe, "-nomipmap", *imgs]
            try:
                subprocess.check_call(cmd)
                logger.info(f"Compressed atlas to {dds_path}")
            except subprocess.CalledProcessError as e:
                logger.error(f"NVCompress failed: {e}")
