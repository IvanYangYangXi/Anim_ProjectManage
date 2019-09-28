#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# items.py
# @Author :  ()
# @Link   :
# @Date   : 7/2/2019, 5:16:22 PM


import sys
from PyQt5 import QtWidgets, uic, Qt
import sip
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
        # self.comboBox_TaskType.currentIndexChanged.connect(
        #     lambda: self.selectionchange(self.comboBox_TaskType))

        # State
        self.comboBox_TaskState = self.ui.comboBox_TaskState
        TaskState = configure.get_DB_Struct('TaskState')
        # 添加多个添加条目
        self.comboBox_TaskState.addItems(TaskState)
        # # 当下拉索引发生改变时发射信号触发绑定的事件
        # self.comboBox_TaskState.currentIndexChanged.connect(
        #     lambda: self.selectionchange(self.comboBox_TaskState))

        # TreePath
        self.HL_Detail_TreePath = self.ui.horizontalLayout_Detail_TreePath


    # 关闭事件
    def closeEvent(self):

        # 将其父设置为空，隐藏控件
        self.setParent(None)

    # -------------- Name -----------------
    # set name
    def setTaskName(self, data):
        self.ui.lineEdit_TaskName.setText(data)

    # def selectionchange(self, editor):
    #     # currentText()：返回选中选项的文本
    #     ct = editor.currentText()
    #     print('Items in the list are:' + ct)

    # -------------- Type -----------------
    # 设置编辑器从模型索引指定的数据模型项中显示和编辑的数据。
    def setTaskType(self, data):
        comboId = 5
        taskType = configure.get_DB_Struct('TaskType')

        if data in taskType:
            comboId = taskType.index(data)

        # 避免不是由用户引起的信号,因此我们使用blockSignals.
        self.comboBox_TaskType.blockSignals(True)
        # ComboBox当前项使用setCurrentIndex()来设置
        self.comboBox_TaskType.setCurrentIndex(comboId)
        self.comboBox_TaskType.blockSignals(False)

    # 从编辑器窗口小部件获取数据
    def getTaskType(self):
        return self.comboBox_TaskType.currentText()

    # -------------- state -----------------
    # 设置编辑器从模型索引指定的数据模型项中显示和编辑的数据。
    def setTaskState(self, data):
        comboId = 0
        TaskState = configure.get_DB_Struct('TaskState')

        if data in TaskState:
            comboId = TaskState.index(data)

        # 避免不是由用户引起的信号,因此我们使用blockSignals.
        self.comboBox_TaskState.blockSignals(True)
        # ComboBox当前项使用setCurrentIndex()来设置
        self.comboBox_TaskState.setCurrentIndex(comboId)
        self.comboBox_TaskState.blockSignals(False)

    # 从编辑器窗口小部件获取数据
    def getTaskState(self):
        return self.comboBox_TaskState.currentText()

    # ---------------- TreePath ----------------
    # 
    def setTreePath(self, data=[]):
        # 删除layout中的所有widget
        # for i in range(self.HL_Detail_TreePath.count()):
        #     if self.HL_Detail_TreePath.itemAt(i) != None:
        #          self.HL_Detail_TreePath.itemAt(i).widget().delete()
        i=0
        for i in range(self.HL_Detail_TreePath.count()):
            widgetItem = self.HL_Detail_TreePath.itemAt(0)
            if widgetItem != None:
                widget = widgetItem.widget()
                # self.HL_Detail_TreePath.removeItem(widgetItem)
                self.HL_Detail_TreePath.removeWidget(widget)
                widget.setParent(None)
                sip.delete(widget)
        i=0
        for i in data:
            lable = QtWidgets.QLabel()
            lable.setText(str(i))
            # lable.setTextFormat(Qt.Qt.AutoText) # 设置自动文本格式
            lable.setOpenExternalLinks(True) # 打开与外部的连接
            # 文本交互形式 鼠标或键盘操作
            lable.setTextInteractionFlags(Qt.Qt.LinksAccessibleByMouse | Qt.Qt.LinksAccessibleByKeyboard)
            lable.setTextInteractionFlags(Qt.Qt.TextBrowserInteraction)
            self.HL_Detail_TreePath.addWidget(lable)

            lable1 = QtWidgets.QLabel()
            lable1.setText('/')
            self.HL_Detail_TreePath.addWidget(lable1)

    # ---------------- label_Detail_Img ----------------

        pix = QPixmap('sexy.jpg')
        lb1 = QLabel(self)
        lb1.setGeometry(0,0,300,200)
        lb1.setStyleSheet("border: 2px solid red")
        lb1.setPixmap(pix)
        lb2 = QLabel(self)
        lb2.setGeometry(0,250,300,200)
        lb2.setPixmap(pix)
        lb2.setStyleSheet("border: 2px solid red") # 便于查看这个标签设置的大小范围
        lb2.setScaledContents(True) # 缩放像素图以填充可用空间
