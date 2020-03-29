#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Skater XL tools for blender.
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

from .sxl import ops, properties, panels


bl_info = {
    "name": "Mod Tools",
    "description": "Tools to create Skater XL content.",
    "author": "Greg Amato [Amatobahn]",
    "version": (1, 0, 1),
    "blender": (2, 80, 0),
    "location": "3dView",
    "warning": "",  # used for warning icon and text in add-ons panel
    "support": "COMMUNITY",
    "wiki_url": "https://github.com/SkaterXLModding/skater-xl-blender",
    "tracker_url": "https://github.com/SkaterXLModding/skater-xl-blender/issues",
    "category": "Skater XL"
}


# We need these functions for blender to recognize an add-on
# and successfully pass their script parser on import
def register():
    ops.register()
    properties.register()
    panels.register()
    print("SXL MOD TOOLS REGISTERED")


def unregister():
    ops.unregister()
    properties.unregister()
    panels.unregister()
    print("SXL MOD TOOL UNREGISTERED")
