#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Skater XL package operators.
"""
# Ensure that compatibility is handled for python 2, 3
from __future__ import division, print_function, absolute_import

__author__ = "Greg Amato"
__url__ = "https://gregamato.dev"
__copyright__ = "Copyright 2019, Greg Amato - Amatobahn"
__credits__ = []
__license__ = "GNU Public License"
__maintainer__ = "Greg Amato"
__status__ = "Development"

import os
import uuid

import bpy
from bpy_extras.io_utils import ExportHelper
import bmesh
import mathutils

from .error_handling import *
from . import utils


class SXLGeneratePoints(bpy.types.Operator):
    bl_idname = "sxl.generate_points"
    bl_label = "Generate Spline Points"
    bl_description = "Generate Spline Points"

    audio_cue = bpy.props.StringProperty()

    @staticmethod
    def look_at(obj, target):
        obj_loc = obj.matrix_world.to_translation()
        direction = target - obj_loc
        quat = direction.to_track_quat('-Z', 'Y')
        obj.rotation_euler = quat.to_euler()

    @staticmethod
    def get_selected_verts(obj):
        """
        Iterate through selected edges and collect vertices
        Args:
            obj: Object to iterate through selected edges

        Returns: List of selected edges
        """
        edge_verts = []

        obj_data = obj.data
        b_mesh = bmesh.from_edit_mesh(obj_data)
        print(b_mesh.select_mode)

        matrix = obj.matrix_world
        if b_mesh.select_mode in [{'EDGE'}]:
            selected_edges = []
            selected_idx = []
            selected_vert = []
            for edge in b_mesh.edges:
                if edge.select:
                    selected_edges.append(edge)
                    for vert in edge.verts:
                        selected_vert.append(vert)
                        selected_idx.append(vert.index)
            start_idx = [v for v in selected_idx if selected_idx.count(v) is 1][0]
            print(start_idx)

            # https://blender.stackexchange.com/questions/72367/how-to-order-a-list-of-vertices-based-upon-position
            # https://blender.stackexchange.com/questions/69796/selection-history-from-shortest-path/69977#69977
            ordered_idx = []
            completed_idx = [start_idx]
            current_idx = start_idx
            while len(completed_idx) != len(selected_edges) + 2:
                for e in b_mesh.edges:
                    if e.select:
                        if e.verts[0].index == current_idx or e.verts[1].index == current_idx:
                            if not e.verts[0].index in completed_idx:
                                to_idx = e.verts[0].index
                                break
                            elif not e.verts[1].index in completed_idx:
                                to_idx = e.verts[1].index
                                break
                ordered_idx.append(current_idx)
                completed_idx.append(to_idx)
                current_idx = to_idx

            print(ordered_idx)

            for idx in ordered_idx:
                vertex = [v for v in selected_vert if v.index == idx][0]
                edge_verts.append(matrix @ vertex.co)
            return edge_verts

        if b_mesh.select_mode == {'VERT'}:
            for vert in b_mesh.verts:
                if vert.select:
                    vector = matrix @ vert.co
                    if vector not in edge_verts:
                        edge_verts.append(vector)

        return edge_verts


    @staticmethod
    def add_point(name, uid, location=(0, 0, 0), parent=None):
        """
        Creates an empty object
        Args:
            name: Name of new object
            uid: Unique Identifier
            location: position in world space to create object at
            parent: object to parent new object to

        Returns: New point Object
        """

        point = bpy.data.objects.new(name, None)
        point.name = "{}_{}".format(point.name.split('.')[0], uid)
        point.empty_display_size = 1
        point.empty_display_type = 'PLAIN_AXES'
        bpy.context.collection.objects.link(point)
        point.location = location

        bpy.context.active_object.select_set(False)
        bpy.data.objects[point.name].select_set(True)
        bpy.data.objects[parent.name].select_set(True)
        bpy.context.view_layer.objects.active = parent
        bpy.ops.object.parent_set(type="OBJECT")
        bpy.context.active_object.select_set(False)

        return point

    def build_grind_points(self, obj):
        """
        Builds all grind points for selected edge group
        Args:
            obj: Object to build points for
        """
        vertex_array = self.get_selected_verts(obj)
        print(vertex_array)
        if len(vertex_array) > 1:
            # Build Grind Root
            grind_root = self.add_point("{}_GrindSpline_{}_Root".format(obj.name, self.audio_cue),
                                        str(uuid.uuid4())[:3],
                                        location=obj.location,
                                        parent=obj)
            # Set grindspline property
            grind_root["grind_spline"] = 1
            grind_root["grind_parent"] = obj.name

            point_uuid = str(uuid.uuid4())[:3]
            for i in range(len(vertex_array)):
                pt = self.add_point("GrindPoint", "{}{}".format(point_uuid, i),
                                    location=vertex_array[i],
                                    parent=grind_root)

            bpy.data.objects[obj.name].select_set(True)
            bpy.context.view_layer.objects.active = obj

    @sxl_exception
    def _execute(self, context):
        if bpy.context.object.mode == "EDIT":
            obj = context.object
            self.build_grind_points(obj)
        else:
            self.report({'WARNING'}, "Grind Splines not generated. Must be in Edit Mode")
        return {'FINISHED'}

    def execute(self, context):
        return_code = self._execute(context)
        return return_code


class SXLGenerateLODs(bpy.types.Operator):
    bl_idname = "sxl.generate_lods"
    bl_label = "Generate Mesh LODs"
    bl_description = "Generate Mesh LODs"

    @staticmethod
    def make_lods(obj):
        if obj is not None:
            for i in range(3):
                new_lod = obj.copy()
                new_lod.name = "{}_LOD{}".format(utils.get_base_name(obj.name), i + 1)
                new_lod.parent = obj

                modifier = new_lod.modifiers.new(name="Decimate", type="DECIMATE")
                modifier.decimate_type = "DISSOLVE"
                modifier.use_dissolve_boundaries = True
                modifier.delimit = {'UV'}
                modifier.angle_limit = 0.174533 * (i + 1)  # 10% * (i + 1)

                triangulate = new_lod.modifiers.new(name="Triangulate", type="TRIANGULATE")
                triangulate.keep_custom_normals = True

                bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Decimate")
                bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Triangulate")

                bpy.context.collection.objects.link(new_lod)

            # Name Base Object
            if '_LOD' not in obj.name:
                obj.name = "{}_LOD0".format(obj.name)

    @sxl_exception
    def _execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            obj = context.object
            self.make_lods(obj)
        else:
            self.report({'WARNING'}, "LODs not generated. Must be in Object Mode")
        return {'FINISHED'}

    def execute(self, context):
        return_code = self._execute(context)
        return return_code


class SXLGenerateCollision(bpy.types.Operator):
    bl_idname = "sxl.generate_collision"
    bl_label = "Generate Collision Shape"
    bl_description = "Generate Collision Shape"

    @staticmethod
    def make_collision_shape(obj):
        if obj is not None:
            collision_obj = obj.copy()
            collision_obj.name = "{}_collision".format(utils.get_base_name(obj.name))
            collision_obj.parent = obj

            modifier = collision_obj.modifiers.new(name="Decimate", type="DECIMATE")
            modifier.decimate_type = "DISSOLVE"
            modifier.angle_limit = 0.174533

            triangulate = collision_obj.modifiers.new(name="Triangulate", type="TRIANGULATE")
            triangulate.keep_custom_normals = True

            bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Decimate")
            bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Triangulate")
            bpy.context.collection.objects.link(collision_obj)

    @sxl_exception
    def _execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            obj = context.object
            self.make_collision_shape(obj)
        else:
            self.report({'WARNING'}, "Collision Shape not generated. Must be in Object Mode")
        return {'FINISHED'}

    def execute(self, context):
        return_code = self._execute(context)
        return return_code


class SXLFinalizeGrinds(bpy.types.Operator):
    bl_idname = "sxl.finalize_grinds"
    bl_label = "Finalize Grinds"
    bl_description = "Finalize Grinds"

    @sxl_exception
    def _execute(self, context):
        prefs = context.preferences.addons['skater-xl-mod-tools'].preferences
        bpy.context.active_object.select_set(False)

        # Check if grind node exists, if not create it.
        if "Grinds" not in bpy.data.objects:
            grinds_pt = bpy.data.objects.new("Grinds", None)
            bpy.context.collection.objects.link(grinds_pt)
        else:
            grinds_pt = bpy.data.objects["Grinds"]
        # Move all grind spline objects to node, maintaining the offset
        objects = bpy.context.scene.objects
        for obj in objects:
            if obj.type == "EMPTY" and obj.get('grind_spline') == 1:
                bpy.context.view_layer.objects.active = obj
                obj.parent = grinds_pt
                bpy.context.active_object.select_set(False)
        return {'FINISHED'}

    def execute(self, context):
        return_code = self._execute(context)
        return return_code


class SXLResetGrinds(bpy.types.Operator):
    bl_idname = "sxl.reset_grinds"
    bl_label = "Reset Grinds"
    bl_description = "Reset Grinds to respective meshes"

    @sxl_exception
    def _execute(self, context):
        bpy.context.active_object.select_set(False)

        # Check if grind node exists, if not return
        if "Grinds" in bpy.data.objects:
            grinds_pt = bpy.data.objects.get("Grinds")
            for obj in bpy.data.objects:
                if obj.parent == grinds_pt and obj.get('grind_spline') == 1:
                    # If the property exists, query the parent, and parent object again
                    grind_parent = bpy.data.objects[obj["grind_parent"]]
                    if grind_parent is not None:
                        bpy.data.objects[obj.name].select_set(True)
                        grind_parent.select_set(True)
                        bpy.context.view_layer.objects.active = grind_parent
                        bpy.ops.object.parent_set(type="OBJECT")
                        bpy.context.active_object.select_set(False)
        return {'FINISHED'}

    def execute(self, context):
        return_code = self._execute(context)
        return return_code


class SXLAssetExport(bpy.types.Operator, ExportHelper):
    bl_idname = "sxl.asset_export"
    bl_label = "Export Asset"
    bl_description = "Export Asset"

    filename_ext = ".fbx"
    filter_glob = bpy.props.StringProperty(default="*.fbx", options={'HIDDEN'}, maxlen=255)

    @sxl_exception
    def _execute(self, context):
        prefs = context.preferences.addons['skater-xl-mod-tools'].preferences
        try:
            if os.path.exists(os.path.split(self.filepath)[0]):
                if not prefs.export_selected_flag:
                    for obj in context.scene.objects:
                        obj.select = obj.type in ['EMPTY', 'ARMATURE', 'MESH']
                else:
                    objects = context.selected_objects
                    for obj in objects:
                        print(obj)
                        utils.get_children(obj, select=True)

                bpy.ops.export_scene.fbx(filepath=self.filepath,
                                         check_existing=True,
                                         use_selection=prefs.export_selected_flag,
                                         object_types={'EMPTY', 'ARMATURE', 'MESH'},
                                         use_tspace=True)
                self.report({'INFO'}, "Export Successful => {}".format(self.filepath))
        except Exception as e:
            self.report({'ERROR'}, e)

        return {'FINISHED'}

    def execute(self, context):
        return_code = self._execute(context)
        return return_code


operations = [
    SXLGeneratePoints,
    SXLGenerateLODs,
    SXLGenerateCollision,
    SXLFinalizeGrinds,
    SXLResetGrinds,
    SXLAssetExport
]


def register():
    for op in operations:
        utils.register(op)


def unregister():
    for op in operations:
        bpy.utils.unregister_class(op)
