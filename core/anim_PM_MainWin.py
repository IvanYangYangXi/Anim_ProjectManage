#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# anim_PM_MainWin.py
# @Author :  ()
# @Link   : 
# @Date   : 7/5/2019, 11:05:30 AM


import sys, os, re
from PyQt5 import QtCore, QtGui, QtWidgets, uic
# from ctypes.wintypes import LONG, HWND, UINT, WPARAM, LPARAM, FILETIME
import shutil # 文件夹操作
import listItems
# import treeModels
from treeModels import *


# ------------------------ 主窗口 class -----------------------------#
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)

        # ----------------------- 概览 ----------------------- #
        item = QtWidgets.QListWidgetItem() # 创建QListWidgetItem对象
        item.setSizeHint(QtCore.QSize(200, 50))  # 设置QListWidgetItem大小
        itemWidget = listItems.ListItem_General_Proj() # itemWidget
        self.ui.listWidget__General_Proj.addItem(item) # 添加item
        self.ui.listWidget__General_Proj.setItemWidget(item, itemWidget)  # 为item设置widget

        # ----------------------- 项目 ----------------------- #
            # ------------------ 任务 ------------------ #
        rootNode_Proj_Task = TreeItem(['', '任务', '类型', '状态', '执行人', '描述', '截止日期', '预估时间（小时）', '结余（小时）', '9'])
        childNode1 = TreeItem(['A1', '1', '2', '3', '4', '5', 'None', '7', '8'], rootNode_Proj_Task)
        childNode2 = TreeItem(['A2', '1', '2', '3', '4', '5', '6', '7'], rootNode_Proj_Task)
        childNode11 = TreeItem(['A21', '1', '2', '3', '4', '5', '6', '7'], childNode1)
        childNode12 = TreeItem(['A21', '1', '2', '3', '4', '5', '6', '7'], childNode1)
        childNode21 = TreeItem(['A21', '1', '2', '3', '4', '5', '6', '7'], childNode2)
        childNode211 = TreeItem(['A21', '1', '2', '3', '4', '5', '6', '7'], childNode21)

        print(rootNode_Proj_Task)

        # 设置 Model
        self.model = TreeModel_Proj_Task(rootNode_Proj_Task)
        self.ui.treeView_Proj_Task.setModel(self.model)

        # 设置 Item 部件
        self.TaskType = ComboBoxDelegate_TaskType()
        self.ui.treeView_Proj_Task.setItemDelegateForColumn(2, self.TaskType)
        self.TaskState = ComboBoxDelegate_TaskState()
        self.ui.treeView_Proj_Task.setItemDelegateForColumn(3, self.TaskState)
        self.TaskDeadline = DateEditDelegate_TaskDeadline()
        self.ui.treeView_Proj_Task.setItemDelegateForColumn(6, self.TaskDeadline)
        

        
    def closeEvent(self, event):
        '''
        重写closeEvent方法
        '''
        event.accept()
        quit()


def main():
    # print(os.path.isdir(amConfigure.getProjectPath()))
    # 启动窗口
    global win
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow(os.path.dirname(os.path.dirname(__file__)) +\
        '/UI/PM_Anim_MainWin.ui')
    win.show()
                   
    sys.exit(app.exec_()) 


if __name__ == '__main__':
    main()