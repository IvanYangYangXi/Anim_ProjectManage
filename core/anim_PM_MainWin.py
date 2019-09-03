#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# anim_PM_MainWin.py
# @Author :  ()
# @Link   :
# @Date   : 7/5/2019, 11:05:30 AM


import sys
import os
import re
from PyQt5 import QtCore, QtGui, QtWidgets, uic
# from ctypes.wintypes import LONG, HWND, UINT, WPARAM, LPARAM, FILETIME
import shutil  # 文件夹操作
import listItems
# import treeModels
from treeModels import *


# ------------------------ 主窗口 class -----------------------------#
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)

        # ----------------------- 概览面板 ----------------------- #
        item = QtWidgets.QListWidgetItem()  # 创建QListWidgetItem对象
        item.setSizeHint(QtCore.QSize(200, 50))  # 设置QListWidgetItem大小
        itemWidget = listItems.ListItem_General_Proj()  # itemWidget
        self.ui.listWidget__General_Proj.addItem(item)  # 添加item
        self.ui.listWidget__General_Proj.setItemWidget(
            item, itemWidget)  # 为item设置widget

        # ----------------------- 项目面板 ----------------------- #
        ## ------------------ 任务面板 ------------------ #
        ### --------------- 任务树 --------------- #
        rootItemData_Proj_Task = configure.get_DB_Struct('rootNode_taskInfo')
        rootNode_Proj_Task = BaseTreeItem(rootItemData_Proj_Task)

        print(rootNode_Proj_Task)

        # 设置 Model
        self.model_Proj_Task = TreeModel_Proj_Task(rootNode_Proj_Task)
        self.ui.treeView_Proj_Task.setModel(self.model_Proj_Task)
        # 右键菜单（treeView_Proj_Task）
        self.createRightMenu_treeView_Proj_Task()

        # 设置 Item 部件
        self.TaskType = ComboBoxDelegate_TaskType()
        self.ui.treeView_Proj_Task.setItemDelegateForColumn(2, self.TaskType)
        self.TaskState = ComboBoxDelegate_TaskState()
        self.ui.treeView_Proj_Task.setItemDelegateForColumn(3, self.TaskState)
        self.TaskDeadline = DateEditDelegate_TaskDeadline()
        self.ui.treeView_Proj_Task.setItemDelegateForColumn(
            6, self.TaskDeadline)

    # 创建右键菜单(treeView_Proj_Task)
    def createRightMenu_treeView_Proj_Task(self):
        # Create right menu for treeview
        self.ui.treeView_Proj_Task.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.treeView_Proj_Task.customContextMenuRequested.connect(
            self.rightMenu_treeView_Proj_Task)

    # 定义右键菜单选项(treeView_Proj_Task)
    def rightMenu_treeView_Proj_Task(self):
        # 创建QMenu
        rightMenu = QtWidgets.QMenu(self.ui.treeView_Proj_Task)
        itemNew = rightMenu.addAction('新建项')
        itemNewChild = rightMenu.addAction('新建子项')
        itemWorkFlow = rightMenu.addAction('快速创建工作流')
        rightMenu.addSeparator() # 分隔器
        itemRefresh = rightMenu.addAction('刷新')
        itemOpenDir = rightMenu.addAction('打开路径')
        itemCollection = rightMenu.addAction('添加到快速访问')
        rightMenu.addSeparator() # 分隔器
        itemDel = rightMenu.addAction('删除（包含所有子项和数据）')

        index = self.ui.treeView_Proj_Task.selectionModel().currentIndex() # 选择的项
        currentItem = self.model_Proj_Task.getItem(index) 
        parentItem = self.model_Proj_Task.parent(index)

        # item1.triggered.connect()
        action = rightMenu.exec_(QtGui.QCursor.pos()) # 在鼠标位置显示

        # 将动作与处理函数相关联 
        # 新建项
        if action == itemNew:
            self.model_Proj_Task.insertRow(parentItem.childCount(), parentItem)
            # else:
            #     showErrorMsg('目录不存在')

    def closeEvent(self, event):
        '''
        重写closeEvent方法
        '''
        event.accept()
        quit()


# 错误信息
def showErrorMsg(msg):
    print(msg)
    win.ui.statusbar.showMessage(msg)

def main():
    # print(os.path.isdir(amConfigure.getProjectPath()))
    # 启动窗口
    global win
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow(os.path.dirname(os.path.dirname(__file__)) +
                     '/UI/PM_Anim_MainWin.ui')
    win.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
