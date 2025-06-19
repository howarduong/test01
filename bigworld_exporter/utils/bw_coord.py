# bigworld_exporter/utils/bw_coord.py

from mathutils import Vector

def to_bigworld(vec, up_axis='Z'):
    """
    把 Blender 坐标 (X, Y, Z) 转为 BigWorld 坐标。
    BigWorld 默认 Y-up，如果 up_axis=='Y'：Z-up→Y-up转换。
    如果 up_axis=='Z'（即不转换），返回原坐标。
    """
    if up_axis == 'Y':
        # Blender Z-up → BigWorld Y-up: (x, y, z) → (x, z, -y)
        return Vector((vec.x, vec.z, -vec.y))
    # Z-up 模式不变
    return vec.copy()
