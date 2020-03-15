#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Skater XL package utilities.
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

import bpy


def is_legacy():
    return bpy.app.version < (2, 80, 0)


def get_children(obj, select=False):
    children = []
    for o in bpy.context.scene.objects:
        if o.parent is obj and o.type in ['EMPTY', 'ARMATURE', 'MESH']:
            if select:
                o.select_set(True)
            children.append(o)
            children.extend(get_children(o, select))
    return children


def get_base_name(name):
    if '_LOD' in name:
        return name[:-5]
    return name


def _make_annotations(cls):
    """Add annotation attribute to class fields to avoid Blender 2.8 warnings"""
    if not hasattr(bpy.app, "version") or bpy.app.version < (2, 80):
        return cls
    bl_props = {k: v for k, v in cls.__dict__.items() if isinstance(v, tuple)}
    if bl_props:
        if '__annotations__' not in cls.__dict__:
            setattr(cls, '__annotations__', {})
        annotations = cls.__dict__['__annotations__']
        for k, v in bl_props.items():
            annotations[k] = v
            delattr(cls, k)
    return cls


def register(cls):
    _make_annotations(cls)
    bpy.utils.register_class(cls)
    return
