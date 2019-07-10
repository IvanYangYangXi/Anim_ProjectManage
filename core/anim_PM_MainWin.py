#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# anim_PM_MainWin.py
# @Author :  ()
# @Link   : 
# @Date   : 7/5/2019, 11:05:30 AM


import sys, os, re
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from ctypes.wintypes import LONG, HWND, UINT, WPARAM, LPARAM, FILETIME
import listItems
import shutil # 文件夹操作


# ------------------------ 主窗口 class -----------------------------#
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)

        # ------------- 概览 ------------- #
        item = QtWidgets.QListWidgetItem() # 创建QListWidgetItem对象
        item.setSizeHint(QtCore.QSize(200, 50))  # 设置QListWidgetItem大小
        itemWidget = listItems.ListItem_General_Proj() # itemWidget
        self.ui.listWidget__General_Proj.addItem(item) # 添加item
        self.ui.listWidget__General_Proj.setItemWidget(item, itemWidget)  # 为item设置widget

        
    def closeEvent(self, event):
        '''
        重写closeEvent方法
        '''
        event.accept()
        quit()


def main():
    # print(os.path.isdir(amConfigure.getProjectPath()))
    # 启动窗口
    global w
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(os.path.dirname(os.path.dirname(__file__)) +\
        '/UI/PM_Anim_MainWin.ui')
    w.show()
                   
    sys.exit(app.exec_()) 


if __name__ == '__main__':
    main()