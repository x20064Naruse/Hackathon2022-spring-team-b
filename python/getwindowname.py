# -*- coding: utf-8 -*-
#これは起動しているウィンドウをすべて列挙するプログラムです
from __future__ import print_function
import win32gui

win32gui.EnumWindows(lambda x, _: print(win32gui.GetWindowText(x)), None)