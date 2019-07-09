#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# items.py
# @Author :  ()
# @Link   : 
# @Date   : 7/2/2019, 5:16:22 PM


import sys
from PyQt5 import QtWidgets, uic


# 项目列表项
class ListItem_General_Proj(QtWidgets.QWidget):
    def __init__(self, uiPath='', parent=None):
        super(ListItem_General_Proj, self).__init__(parent)

        uiPath = './UI/listItem_General_Proj.ui'
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)