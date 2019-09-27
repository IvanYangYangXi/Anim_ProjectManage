#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# items.py
# @Author :  ()
# @Link   :
# @Date   : 7/2/2019, 5:16:22 PM


import sys
from PyQt5 import QtWidgets, uic
import configure


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

        # Type
        self.comboBox_TaskType = self.ui.comboBox_TaskType
        taskType = configure.get_DB_Struct('TaskType')
        # 添加多个添加条目
        self.comboBox_TaskType.addItems(taskType)
        # 当下拉索引发生改变时发射信号触发绑定的事件
        self.comboBox_TaskType.currentIndexChanged.connect(
            lambda: self.selectionchange(self.comboBox_TaskType))


    # 关闭事件
    def closeEvent(self):

        # 将其父设置为空，隐藏控件
        self.setParent(None)

    def createEditor(self, parent, option, index):

        taskType = configure.get_DB_Struct('TaskType')

        editor = QtWidgets.QComboBox(parent)
        # editor.addItem('项目')
        # 多个添加条目
        editor.addItems(taskType)
        # 当下拉索引发生改变时发射信号触发绑定的事件
        editor.currentIndexChanged.connect(
            lambda: self.selectionchange(editor))

        return editor

    def selectionchange(self, editor):
        # currentText()：返回选中选项的文本
        ct = editor.currentText()
        print('Items in the list are:' + ct)

    # 设置编辑器从模型索引指定的数据模型项中显示和编辑的数据。
    def setEditorData(self, editor, index):
        data = index.model().data(index, QtCore.Qt.EditRole)
        comboId = 5
        taskType = configure.get_DB_Struct('TaskType')

        if data in taskType:
            comboId = taskType.index(data)

        # 避免不是由用户引起的信号,因此我们使用blockSignals.
        editor.blockSignals(True)
        # ComboBox当前项使用setCurrentIndex()来设置
        editor.setCurrentIndex(comboId)
        editor.blockSignals(False)

    # 从编辑器窗口小部件获取数据，并将其存储在项索引处的指定模型中。
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)
