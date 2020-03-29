#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Skater XL properties.
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

from . import utils


class SXLSceneProperties(bpy.types.PropertyGroup):

    # MAIN PANEL PROPERTIES
    spline_menu = bpy.props.BoolProperty(default=True)
    file_menu = bpy.props.BoolProperty(default=True)
    lod_menu = bpy.props.BoolProperty(default=True)
    collision_menu = bpy.props.BoolProperty(default=True)

    # SPLINE PROPERTIES
    audio_cues = bpy.props.EnumProperty(
        items=[("Metal", "Metal", "", "", 0), ("Concrete", "Concrete", "", "", 1), ("Wood", "Wood", "", "", 2)],
        name="Audio Cue Material",
        description="Audio Cue for grind type"
    )

    # EXPORTER PROPERTIES
    export_selected_flag = bpy.props.BoolProperty(default=False)
    export_animation_flag = bpy.props.BoolProperty(default=False)


class SXLAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = "skater-xl-mod-tools"

    # MAIN PANEL PERSISTENCE
    spline_menu = bpy.props.BoolProperty(default=True)
    spline_finalized = bpy.props.BoolProperty(default=False)
    lod_menu = bpy.props.BoolProperty(default=True)
    collision_menu = bpy.props.BoolProperty(default=True)

    # EXPORT PREFERENCES
    export_selected_flag = bpy.props.BoolProperty(default=False)
    export_animation_flag = bpy.props.BoolProperty(default=False)
    # export_save = bpy.props.BoolProperty(default=False)

    def draw(self, context):
        layout = self.layout
        column = layout.column()

        box = column.box()
        box.row().label(text="Export Options")
        box.row().prop(self, "export_save", text="Save On Export")
        box.row().prop(self, "export_selected_flag", text="Export Selected")
        box.row().prop(self, "export_animation_flag", text="Export Animation")


properties = [
    SXLSceneProperties,
    SXLAddonPreferences
]


def register():
    for prop in properties:
        utils.register(prop)
    bpy.types.Scene.SXL = bpy.props.PointerProperty(type=SXLSceneProperties)


def unregister():
    for prop in properties:
        bpy.utils.unregister_class(prop)
    del bpy.types.Scene.SXL
