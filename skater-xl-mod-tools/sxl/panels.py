#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Skater XL package panels.
"""
# Ensure that compatibility is handled for python 2, 3
from __future__ import division, print_function, absolute_import

__author__ = "Greg Amato"
__url__ = "https://gregamato.dev"
__copyright__ = "Copyright 2019-2020, Greg Amato - Amatobahn"
__credits__ = []
__license__ = "GNU Public License"
__maintainer__ = "Greg Amato"
__status__ = "Development"

import bpy

from .ops import *
from . import utils


class SXLPanel(bpy.types.Panel):
    bl_idname = "SXL_PT_panel"
    bl_label = "Skater XL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS" if bpy.app.version < (2, 80, 0) else "UI"
    bl_category = "Skater XL"

    def draw_header(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.operator("wm.url_open", icon="URL").url = __url__
        row.operator("wm.url_open", icon="INFO").url = "https://github.com/Amatobahn/skater-xl-blender/issues"
        row.operator("wm.url_open", icon="QUESTION").url = "https://discord.gg/f2m29U5"
        row.separator()

    def draw(self, context):
        prefs = context.preferences.addons['skater-xl-mod-tools'].preferences
        sxl = context.scene.SXL
        layout = self.layout

        # SPLINE GENERATION
        box = layout.box()
        column = box.column()
        row = column.row()
        row.scale_y = 1.2
        row.label(text="Grind Splines", icon="NOCURVE")

        row = column.split(factor=0.5)
        row.label(text="Audio Cue", icon="PLAY_SOUND")
        row.scale_y = 1.2
        row.prop(sxl, "audio_cues", text="")

        row = column.row()
        row.separator()
        row = column.row()
        row.scale_y = 1.2
        row.operator("sxl.generate_points", icon="OUTLINER_DATA_EMPTY").audio_cue = sxl.audio_cues
        column.separator()
        row = column.row()
        row.scale_y = 1.2
        row.operator("sxl.finalize_grinds", icon="DECORATE_LOCKED")
        row = column.row()
        row.scale_y = 1.2
        row.operator("sxl.reset_grinds", icon="FILE_REFRESH")


class SXLExperimentalPanel(bpy.types.Panel):
    bl_idname = "SXL_PT_experimental_panel"
    bl_label = "Skater XL [EXPERIMENTAL]"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS" if bpy.app.version < (2, 80, 0) else "UI"
    bl_category = "Skater XL"

    def draw(self, context):
        prefs = context.preferences.addons['skater-xl-mod-tools'].preferences

        layout = self.layout

        box = layout.box()
        row = box.row()
        row.prop(prefs, "lod_menu", text="Level of Detail",
                 icon="TRIA_DOWN" if prefs.lod_menu else "TRIA_RIGHT",
                 icon_only=True, emboss=False)
        if prefs.lod_menu:
            row = box.row()
            row.scale_y = 1.2
            row.operator("sxl.generate_lods", icon="MOD_EXPLODE")

        box = layout.box()
        row = box.row()
        row.prop(prefs, "collision_menu", text="Collision",
                 icon="TRIA_DOWN" if prefs.collision_menu else "TRIA_RIGHT",
                 icon_only=True, emboss=False)
        if prefs.collision_menu:
            row = box.row()
            row.scale_y = 1.2
            row.operator("sxl.generate_collision", icon="AUTOMERGE_ON")


class SXLExportPanel(bpy.types.Panel):
    bl_idname = "SXL_PT_export_panel"
    bl_label = "Skater XL [EXPORT]"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS" if bpy.app.version < (2, 80, 0) else "UI"
    bl_category = "Skater XL"

    def draw(self, context):
        prefs = context.preferences.addons['skater-xl-mod-tools'].preferences
        layout = self.layout

        # Export Options
        box = layout.box()
        column = box.column()
        row = column.row()
        row.label(text="Export Options")
        # Export Flag Options
        row = column.row(align=True)
        row.prop(prefs, "export_selected_flag", text="Export Selected")
        row.prop(prefs, "export_animation_flag", text="Export Animation")

        # Export Asset
        row = layout.row()
        row.scale_y = 1.2
        row.operator("sxl.asset_export", text="Export", icon="EXPORT")


panels = [
    SXLPanel,
    SXLExperimentalPanel,
    SXLExportPanel
]


def register():
    for panel in panels:
        utils.register(panel)


def unregister():
    for panel in panels:
        bpy.utils.unregister_class(panel)
