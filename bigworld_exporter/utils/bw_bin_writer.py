import struct
from mathutils import Vector  # 确保引入 Vector

def _pack_floats(fp, floats):
    # 4 字节浮点对齐
    fp.write(struct.pack(f"<{len(floats)}f", *floats))

def _pack_uints(fp, ints):
    # 4 字节无符号整型对齐
    fp.write(struct.pack(f"<{len(ints)}I", *ints))

class VertexWriter:
    def __init__(self, bin_prefix):
        # 覆盖写入
        self.fp = open(bin_prefix + ".bin", "wb")

    def write_vertex(self, vertex, settings):
        """
        vertex: dict or object，含
          pos: (x,y,z), normal: (x,y,z), tangent: (x,y,z, w),
          uv: [(u,v),...], color: (r,g,b,a), skin: [(bone_idx, weight),...]
        settings: BWExportSettings，决定写哪些属性
        """
        # 如果传入的是 Vector 对象，则自动构造一个简单的包装对象，默认其它属性取默认值
        if isinstance(vertex, Vector):
            # 定义一个简单的容器类型
            class SimpleVertex:
                pass
            simple_vertex = SimpleVertex()
            simple_vertex.pos = vertex.copy()  # 设置位置
            simple_vertex.normal = [0.0, 0.0, 0.0]          # 默认法线
            simple_vertex.tangent = [0.0, 0.0, 0.0, 0.0]      # 默认切线
            simple_vertex.uvs = []                           # 默认没有UV数据，可根据需要修改为 [[0.0, 0.0]]
            simple_vertex.color = [1.0, 1.0, 1.0, 1.0]       # 默认颜色白色
            simple_vertex.skin = []                          # 默认骨骼数据为空
            vertex = simple_vertex

        # 写入位置数据
        _pack_floats(self.fp, vertex.pos)
        # 写入法线
        if settings.include_normals:
            _pack_floats(self.fp, vertex.normal)
        # 写入切线
        if settings.include_tangents:
            _pack_floats(self.fp, vertex.tangent)
        # 写入 UV 数据
        if settings.include_uvs:
            for uv in vertex.uvs:
                _pack_floats(self.fp, uv)
        # 写入颜色
        if settings.include_vcolor:
            _pack_floats(self.fp, vertex.color)
        # 写入骨骼数据（如果有），假设最多4个影响
        if settings.include_skin:
            for idx, w in vertex.skin:
                _pack_uints(self.fp, [idx])
                _pack_floats(self.fp, [w])

    def close(self):
        self.fp.close()

class IndexWriter:
    def __init__(self, bin_prefix):
        # 以追加形式写入
        self.fp = open(bin_prefix + ".bin", "ab")

    def write_indices(self, indices):
        # 32 位索引
        _pack_uints(self.fp, indices)

    def close(self):
        self.fp.close()

# 模块级包装函数，保持原有调用方式
def write_vertex(vert_writer, vertex, settings):
    """
    模块级包装函数，将导入的 VertexWriter 实例的方法打包为模块级函数，
    这样旧代码可继续使用 bw_bin_writer.write_vertex(vert_writer, vertex, settings)
    """
    return vert_writer.write_vertex(vertex, settings)
