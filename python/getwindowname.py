# -*- coding: utf-8 -*-

from __future__ import print_function
import win32gui

win32gui.EnumWindows(lambda x, _: print(win32gui.GetWindowText(x)), None)