# bigworld_exporter/utils/bw_lod.py

import bpy

def collect_manual_lods(base_obj):
    """
    按命名约定收集同名 _LOD0/_LOD1... 对象
    返回 [(0, obj0), (1, obj1), ...]
    """
    name = base_obj.name.split('_LOD')[0]
    lods = []
    for o in bpy.data.objects:
        if o.name.startswith(name + "_LOD"):
            try:
                idx = int(o.name.split('_LOD')[1])
                lods.append((idx, o))
            except:
                continue
    return sorted(lods, key=lambda x: x[0])

def auto_decimate(obj, ratio):
    """
    对 obj 应用临时 Decimate Modifier，并返回新对象
    """
    dup = obj.copy()
    dup.data = obj.data.copy()
    mod = dup.modifiers.new("LOD_Dec", 'DECIMATE')
    mod.ratio = ratio
    # 应用后立即移除 modifier
    bpy.context.view_layer.objects.active = dup
    bpy.ops.object.modifier_apply(modifier=mod.name)
    return dup
