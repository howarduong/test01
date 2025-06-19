# bigworld_exporter/ops/export_model.py

import os, traceback
import bpy
from bpy.types import Operator
from ..properties import BWExportSettings
from ..utils import (
    bw_mesh_split, bw_coord, bw_xml_writer, bw_bin_writer,
    bw_material_map, bw_collision, bw_logging, bw_pipeline_hooks
)

logger = bw_logging.get_logger()

class BW_OT_export_model(Operator):
    bl_idname = "bw.export_model"
    bl_label = "Export Model/Visual/Primitives"
    bl_description = "Export selected objects to BigWorld .model/.visual/.primitives"
    bl_options = {'REGISTER'}

    def execute(self, context):
        settings: BWExportSettings = context.scene.bw_export
        prefs = context.preferences.addons["bigworld_exporter"].preferences

        root = bpy.path.abspath(settings.resource_root)
        os.makedirs(root, exist_ok=True)

        wm = context.window_manager
        try:
            # Prepare XML & BIN writers
            model_writer = bw_xml_writer.ModelWriter(root, settings.model_name)
            visual_writer = bw_xml_writer.VisualWriter(root, settings.model_name)
            vert_writer = bw_bin_writer.VertexWriter(visual_writer.bin_path)
            idx_writer = bw_bin_writer.IndexWriter(visual_writer.bin_path)

            # Collect targets
            meshes = [o for o in context.selected_objects if o.type == 'MESH']
            empties = [o for o in context.selected_objects if o.type == 'EMPTY']
            arms = [o for o in context.selected_objects if o.type == 'ARMATURE']

            total = len(meshes) + len(arms) + (1 if settings.export_primitives else 0)
            wm.progress_begin(0, total)

            # 1) .model: all nodes
            for i, obj in enumerate(meshes + empties + arms):
                model_writer.add_node(obj, bw_coord.to_bigworld, obj.parent)
                wm.progress_update(i)

            model_writer.save()
            self.report({'INFO'}, ".model export done")

            # 2) .visual + bins: each mesh → chunks
            step = len(meshes)
            for i, obj in enumerate(meshes):
                chunks = bw_mesh_split.split_mesh(
                    obj, settings.max_verts, settings.max_indices,
                    settings.grouping
                )
                for cid, ch in enumerate(chunks):
                    visual_writer.add_chunk(obj.name, cid, ch.mat_id)
                    for v in ch.vertices:
                        bw_bin_writer.write_vertex(vert_writer, v, settings)
                    idx_writer.write_indices(ch.indices)
                wm.progress_update(i + len(arms))
            visual_writer.save()
            vert_writer.close(); idx_writer.close()
            self.report({'INFO'}, ".visual export done")

            # 3) .primitives: collision
            if settings.export_primitives:
                prim_writer = bw_xml_writer.PrimitiveWriter(root, settings.model_name)
                coll_objs = [
                    o for o in context.scene.objects
                    if o.get("bw_collision") and
                       bpy.path.fnmatch.fnmatch(o.name, settings.collision_filter)
                ]
                for j, obj in enumerate(coll_objs):
                    data = bw_collision.generate(obj, settings.up_axis)
                    prim_writer.add(obj.name, data)
                    wm.progress_update(step + j)
                prim_writer.save()
                self.report({'INFO'}, ".primitives export done")

            wm.progress_end()

            # 4) materials
            if settings.export_materials:
                for mat in bpy.data.materials:
                    bw_material_map.export(mat, root)
                self.report({'INFO'}, ".material export done")

            # 5) Post-Tools pipeline
            if settings.post_tools:
                bw_pipeline_hooks.run_all(
                    root,
                    prefs.convert_model_script,
                    prefs.convert_materials_script,
                    prefs.texture_tool_executable,
                    prefs.package_builder_script,
                    prefs.chunk_viz_script,
                    prefs.resource_scanner_script,
                    prefs.enable_vcs_hook
                )
                self.report({'INFO'}, "Post-Tools pipeline finished")

            return {'FINISHED'}

        except Exception as e:
            wm.progress_end()
            logger.error("Export failed", exc_info=True)
            self.report({'ERROR'}, f"Export failed: {e}")
            return {'CANCELLED'}

def register_export_model():
    bpy.utils.register_class(BW_OT_export_model)

def unregister_export_model():
    bpy.utils.unregister_class(BW_OT_export_model)
