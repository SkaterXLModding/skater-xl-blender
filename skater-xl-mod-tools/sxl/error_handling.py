#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Skater XL package error handling.
"""
# Ensure that compatibility is handled for python 2, 3
from __future__ import division, print_function, absolute_import

__author__ = "Greg Amato"
__url__ = "https://gregamato.dev"
__copyright__ = "Copyright 2019, Greg Amato - Amatobahn"
__credits__ = []
__license__ = "MIT"
__maintainer__ = "Greg Amato"
__status__ = "Development"

import functools


class SXLException(Exception):
    pass


class SXLModeError(SXLException):
    pass


def sxl_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SXLException as e:
            print("SXL EXCEPTION: {}".format(e))
    return wrapper

