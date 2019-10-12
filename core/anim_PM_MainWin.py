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
import loadWidgets
import configure
from treeModels import *


# ------------------------ 主窗口 class -----------------------------#
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)
        # 检查工程目录是否存在,不存在则设置工程目录
        if not os.path.isdir(configure.getProjectPath()):
            SetProjectPath()

        # ---------------------------- 概览面板 ---------------------------- #
        self.item = QtWidgets.QListWidgetItem()  # 创建QListWidgetItem对象
        self.item.setSizeHint(QtCore.QSize(200, 50))  # 设置QListWidgetItem大小
        self.itemWidget = loadWidgets.ListItem_General_Proj()  # itemWidget
        self.ui.listWidget_General_Proj.addItem(self.item)  # 添加item
        self.ui.listWidget_General_Proj.setItemWidget(
            self.item, self.itemWidget)  # 为item设置widget

        # -------------------------- 详细信息面板 -------------------------- #
        self.detailPage_Proj_Task = loadWidgets.DetailPage()  # Widget- DetailPage 详细信息面板

        # ---------------------------- 项目面板 ---------------------------- #
        ## ------------------ 任务面板 ------------------ #
        ### --------------- 任务树 --------------- #
        self.rootItemData_Proj_Task = configure.get_DB_Struct(
            'rootNode_taskInfo')
        self.rootNode_Proj_Task = BaseTreeItem(self.rootItemData_Proj_Task)

        print(self.rootNode_Proj_Task)
        self.ui.treeView_Proj_Task.setColumnWidth(0,200) # 不起作用！！！？

        # 设置 Model
        self.model_Proj_Task = TreeModel_Proj_Task(self.rootNode_Proj_Task)
        self.model_Proj_Task.func = self.currentIndexDataChanged # 数据更新时调用的函数
        self.ui.treeView_Proj_Task.setModel(self.model_Proj_Task)
        self.detailPage_Proj_Task.model_Proj_Task = self.model_Proj_Task # 把树model传入detailPage

        # treeView_Proj_Task item 点击事件
        self.ui.treeView_Proj_Task.clicked.connect(self.taskTreeItemClicked)
        # treeView_Proj_Task item 双击事件
        self.ui.treeView_Proj_Task.doubleClicked.connect(self.taskTreeItemDoubleClicked)
        # 右键菜单（treeView_Proj_Task）
        self.createRightMenu_treeView_Proj_Task()

        # 设置 Item 部件
        self.delegate = range(10)
        self.setDelegate()
        self.lastSelectIndex = None
        # self.TaskDeadline = DateEditDelegate()
        # self.ui.treeView_Proj_Task.setItemDelegateForColumn(
        #     7, self.TaskDeadline)


    # 设置 Item 部件
    def setDelegate(self):
        dataTypes = configure.get_DB_Struct('dataTypes')
        # print(dataTypes)
        dataTypes = dataTypes[4:]
        # print(dataTypes)
        self.delegate = range(len(dataTypes))
        for i in range(len(dataTypes)):
            # print(dataTypes[i])
            if dataTypes[i] == 'int':
                self.delegate[i] = SpinBoxDelegate()
                self.ui.treeView_Proj_Task.setItemDelegateForColumn(i, self.delegate[i])
            elif dataTypes[i] == 'float':
                self.delegate[i] = DoubleSpinBoxDelegate()
                self.ui.treeView_Proj_Task.setItemDelegateForColumn(i, self.delegate[i])
            elif dataTypes[i] == 'date':
                self.delegate[i] = DateEditDelegate()
                self.ui.treeView_Proj_Task.setItemDelegateForColumn(i, self.delegate[i])
            elif dataTypes[i] == 'string':
                self.delegate[i] = StringLineEditDelegate()
                self.ui.treeView_Proj_Task.setItemDelegateForColumn(i, self.delegate[i])
            elif dataTypes[i].split(':')[0] == 'combo':
                self.delegate[i] = ComboBoxDelegate(dataTypes[i].split(':')[1], dataTypes[i].split(':')[2])
                self.ui.treeView_Proj_Task.setItemDelegateForColumn(i, self.delegate[i])
    
    # @QtCore.pyqtSlot()
    def currentIndexDataChanged(self):
        # print('currentIndexDataChanged')
        self.setDetailPageInfo(self.ui.treeView_Proj_Task.currentIndex())

    # 设置 详细信息面板 内容
    def setDetailPageInfo(self, index):
        if index == QtCore.QModelIndex():
            index = self.lastSelectIndex
        if index != None: 
            currentItem = self.model_Proj_Task.getItem(index) 
            self.detailPage_Proj_Task.datas = currentItem.datas()
            self.detailPage_Proj_Task.currentIndex = index

            labels = configure.get_DB_Struct("rootNode_taskInfo")
            # ---------- 信息 -----------
            # taskName
            if u'任务' in labels:
                num = labels.index(u'任务')
                self.detailPage_Proj_Task.setTaskName(currentItem.datas()[num])
            # type
            if u'类型' in labels:
                num = labels.index(u'类型')
                self.detailPage_Proj_Task.setTaskType(currentItem.datas()[num])
            # state
            if u'状态' in labels:
                num = labels.index(u'状态')
                self.detailPage_Proj_Task.setTaskState(currentItem.datas()[num])
            # treePath
            if u'任务' in labels:
                num = labels.index(u'任务')
                treePath = [currentItem.datas()[num]]
                parentItem = currentItem.parent()
                while parentItem != None:
                    treePath.insert(0, parentItem.datas()[num])
                    parentItem = parentItem.parent()
                treePath = treePath[1:]
                self.detailPage_Proj_Task.setTreePath(treePath)
            # Detail_Img
            if u'缩略图' in labels:
                num = labels.index(u'缩略图')
                self.detailPage_Proj_Task.setDetail_Img(currentItem.datas()[num])
            # FL_Info
            labels = configure.get_DB_Struct('rootNode_taskInfo')
            datas = currentItem.datas()
            dataTypes = configure.get_DB_Struct('dataTypes')
            self.detailPage_Proj_Task.setFL_Info(labels, datas, dataTypes)

            # ---------- 文件 -----------
            # fileList_Path
            self.detailPage_Proj_Task.fileList._path = configure.getProjectPath() + '/data/Content/%s'%currentItem.datas()[0]
            self.detailPage_Proj_Task.fileList.updateList() # 更新文件列表

    # treeView_Proj_Task item 点击事件
    def taskTreeItemClicked(self, index):
        self.lastSelectIndex = index
        # 获取当前项的首列 index
        newIndex = self.model_Proj_Task.getColumnIndex(index)
        self.model_Proj_Task.updateChild(newIndex) # 更新子项

        # 展开子项
        if self.model_Proj_Task.rowCount(newIndex) > 0:
            self.ui.treeView_Proj_Task.expand(newIndex)

        # 设置 详细信息面板 内容
        self.setDetailPageInfo(index)

    # treeView_Proj_Task item 双击事件
    def taskTreeItemDoubleClicked(self, index):
        self.lastSelectIndex = index
        # QtWidgets.QBoxLayout.itemAt(1).Widget().close() / .show()
        # 添加 详细信息面板UI 到 horizontalLayout_Centralwidget
        self.ui.horizontalLayout_Centralwidget.addWidget(self.detailPage_Proj_Task)

        # 设置 详细信息面板 内容
        self.setDetailPageInfo(index)

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
        itemInsert = rightMenu.addAction('插入项')
        itemWorkFlow = rightMenu.addAction('快速创建工作流')
        rightMenu.addSeparator()  # 分隔器
        itemRefresh = rightMenu.addAction('刷新')
        itemOpenDir = rightMenu.addAction('打开路径')
        itemCollection = rightMenu.addAction('添加到快速访问')
        rightMenu.addSeparator()  # 分隔器
        itemDel = rightMenu.addAction('删除（包含所有子项和数据）')

        indexes = self.ui.treeView_Proj_Task.selectedIndexes()  # 获取所有选择单项
        index = self.ui.treeView_Proj_Task.selectionModel().currentIndex()  # 选择的项
        selectRowCount = len(indexes)/self.model_Proj_Task.columnCount(index) # 选择的行数
        # print(selectRowCount)
        if selectRowCount == 1: # 选择一行
            currentItem = self.model_Proj_Task.getItem(index)
            currentItems = [currentItem]
            rowIndexes = [index]
            parentIndex = self.model_Proj_Task.parent(index)
        elif selectRowCount == 0: # 选择0行(父级为root项)
            currentItem = None
            currentItems = []
            parentIndex = QtCore.QModelIndex()
        else: # 选择多行(父级为空)
            currentItems = []
            rowIndexes = []
            for i in range(selectRowCount):
                rowIndexes.append(indexes[i*self.model_Proj_Task.columnCount(index)])
            for i in rowIndexes:
                currentItem = self.model_Proj_Task.getItem(i)
                currentItems.append(currentItem)
            currentItem = self.model_Proj_Task.getItem(index)
            parentIndex = None

        # 禁用菜单项
        if parentIndex == None: # 父项不存在时（选择多行）
            itemNew.setEnabled(False)
            itemNewChild.setEnabled(False)
            itemInsert.setEnabled(False)
            itemRefresh.setEnabled(False)
            itemCollection.setEnabled(False)
        if currentItem == None: # 无选择项时（选择0行(父级为root项)）
            itemNewChild.setEnabled(False)
            itemOpenDir.setEnabled(False)
            itemInsert.setEnabled(False)
            itemDel.setEnabled(False)

            # item1.triggered.connect()
        action = rightMenu.exec_(QtGui.QCursor.pos())  # 在鼠标位置显示

        # 将动作与处理函数相关联
        # 新建项(在末端添加)
        if action == itemNew:
            newItemIndex = self.model_Proj_Task.insertRow(self.model_Proj_Task.rowCount(parentIndex), parentIndex)
            self.ui.treeView_Proj_Task.setCurrentIndex(newItemIndex)
            # else:
            #     showErrorMsg('目录不存在')
        # 新建子项
        if action == itemNewChild:
            for i in range(selectRowCount):
                newItemIndex = self.model_Proj_Task.insertRow(currentItems[i].childCount(), rowIndexes[i])
                self.ui.treeView_Proj_Task.setCurrentIndex(newItemIndex)
        # 插入项
        if action == itemInsert:
            newItemIndex = self.model_Proj_Task.insertRow(currentItem.row(), parentIndex)
            self.ui.treeView_Proj_Task.setCurrentIndex(newItemIndex)
        # 刷新
        if action == itemRefresh:
            self.model_Proj_Task.updateChild(parentIndex) # 更新子项
        # 删除（包含所有子项和数据）
        if action == itemDel:
            reply = QtWidgets.QMessageBox.warning(
                self, "警告",  "确认删除选择项?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply:
                for i in range(selectRowCount):
                    # os.removedirs(path)    # 递归删除文件夹 (i, o) in (currentItems, rowIndexes)
                    self.model_Proj_Task.removeRow(
                        currentItems[i].row(), self.model_Proj_Task.parent(rowIndexes[i]))

    def closeEvent(self, event):
        '''
        重写closeEvent方法
        '''
        event.accept()
        quit()


# 选择文件夹
def browse():
    directory = ''
    if configure.getProjectPath() != None:
        if os.path.isdir(configure.getProjectPath()):
            directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Find Dir",
                                                                   configure.getProjectPath())
        else:
            directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Find Dir",
                                                                   QtCore.QDir.currentPath())
    else:
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Find Dir",
                                                               QtCore.QDir.currentPath())

    return directory


# 设置工程目录
def SetProjectPath():
    directory = browse()
    if directory != '':
        configure.setProjectPath(directory)
        configure.createProjectConfig()
    elif not os.path.isdir(configure.getProjectPath()):
        showErrorMsg('工程目录不存在')
        # w.close() # 退出窗口程序


# 错误信息
def showErrorMsg(msg):
    print(msg)
    win.ui.statusbar.showMessage(msg)


def main():
    # print(os.path.isdir(configure.getProjectPath()))
    # 启动窗口
    global win
    app = QtWidgets.QApplication(sys.argv)
    # win = MainWindow(os.path.dirname(os.path.dirname(__file__)) +
    #                  '/UI/PM_Anim_MainWin.ui')
    win = MainWindow('./UI/PM_Anim_MainWin.ui')
    win.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
