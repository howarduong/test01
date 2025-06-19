# bigworld_exporter/ops/create_objects.py

import bpy
import bmesh
from mathutils import Vector
from bpy.types import Operator
from bpy.props import EnumProperty, StringProperty
from ..utils.bw_logging import get_logger

logger = get_logger(__name__)

class BW_OT_create_primitive(Operator):
    bl_idname = "bw.create_primitive"
    bl_label = "Add Primitive with Collision"
    bl_description = "Add a collision primitive and tag for export"
    bl_options = {'REGISTER', 'UNDO'}

    prim_type: EnumProperty(
        name="Primitive Type",
        items=[('BOX',"Box",''),('CAPSULE',"Capsule",''),('HULL',"Convex Hull",'')],
        default='BOX'
    )
    name: StringProperty(
        name="Object Name",
        default="Collision"
    )

    def execute(self, context):
        mesh = bpy.data.meshes.new(self.name + "_mesh")
        obj = bpy.data.objects.new(self.name, mesh)
        context.collection.objects.link(obj)
        bm = bmesh.new()
        if self.prim_type == 'BOX':
            bmesh.ops.create_cube(bm, size=1.0)
        elif self.prim_type == 'CAPSULE':
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False,
                                  segments=16, diameter1=1.0, diameter2=1.0, depth=1.0)
        else:
            bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.convex_hull(bm, input=bm.verts)
        bm.to_mesh(mesh); bm.free()

        obj["bw_collision"] = self.prim_type
        logger.info(f"Primitive created: {obj.name} of type {self.prim_type}")
        self.report({'INFO'}, f"Created {self.prim_type} primitive: {obj.name}")
        return {'FINISHED'}

def register_create_ops():
    bpy.utils.register_class(BW_OT_create_primitive)

def unregister_create_ops():
    bpy.utils.unregister_class(BW_OT_create_primitive)
