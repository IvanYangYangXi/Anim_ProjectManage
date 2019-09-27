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

        if uiPath == '':
            uiPath = './UI/listItem_General_Proj.ui'
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)


# 详细信息面板UI
class DetailPage(QtWidgets.QWidget):
    def __init__(self, uiPath='', parent=None):
        super(DetailPage, self).__init__(parent)

        if uiPath == '':
            uiPath = './UI/Widget_DetailPage.ui'
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)

        # 关闭按钮 点击事件
        self.closeButton = self.ui.pushButton_Detail_Close
        self.closeButton.setToolTip('关闭详细面板')
        self.closeButton.clicked.connect(self.closeEvent)


    # 关闭事件
    def closeEvent(self):

        # 将其父设置为空，隐藏控件
        self.setParent(None)