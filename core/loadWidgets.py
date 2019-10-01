#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# items.py
# @Author :  ()
# @Link   :
# @Date   : 7/2/2019, 5:16:22 PM


import sys, os
from PyQt5 import QtWidgets, uic, Qt, QtCore, QtGui
import sip
import platform
import subprocess
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

        # TypeIcon
        self.label_TypeIcon = self.ui.label_TypeIcon

        # Detail_Img
        # QtWidgets.QHBoxLayout.replaceWidget()
        self.label_Detail_Img = ClickLabel()
        self.label_Detail_Img.setGeometry(1, 1, 135, 85)
        self.label_Detail_Img.setMinimumSize(135, 85)
        self.label_Detail_Img.setMaximumSize(135, 85)
        # 替换并移除控件
        self.ui.horizontalLayout_Detail_Img.replaceWidget(self.ui.label_Detail_Img, self.label_Detail_Img)
        self.label_Detail_Img = self.ui.label_Detail_Img
        # self.ui.horizontalLayout_Detail_Img.removeWidget(self.ui.label_Detail_Img)
        # self.ui.label_Detail_Img.setParent(None)
        # sip.delete(self.ui.label_Detail_Img)

        # -------- Info ---------
        self.FL_Info = self.ui.formLayout_Detail_Info


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

        self.setTypeIcon() # 设置 Type 图标

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
        for i in range(self.HL_Detail_TreePath.count()):
            widgetItem = self.HL_Detail_TreePath.itemAt(0)
            if widgetItem != None:
                widget = widgetItem.widget()
                # self.HL_Detail_TreePath.removeItem(widgetItem)
                self.HL_Detail_TreePath.removeWidget(widget)
                widget.setParent(None)
                sip.delete(widget)
        for i in data:
            lable = QtWidgets.QLabel()
            lable.setText(" <a href='none' style='color:blue'>%s</a>"%str(i))
            lable.setTextFormat(Qt.Qt.AutoText) # 设置自动文本格式
            lable.setOpenExternalLinks(True) # 打开与外部的连接,允许访问超链接
            # lable.linkActivated.connect(self.link_clicked)#针对链接点击事件
            # 文本交互形式 鼠标或键盘操作
            lable.setTextInteractionFlags(Qt.Qt.LinksAccessibleByMouse | Qt.Qt.LinksAccessibleByKeyboard)
            lable.setTextInteractionFlags(Qt.Qt.TextBrowserInteraction)
            self.HL_Detail_TreePath.addWidget(lable)

            lable1 = QtWidgets.QLabel()
            lable1.setText('/')
            self.HL_Detail_TreePath.addWidget(lable1)

    # ---------------- label_TypeIcon ----------------
    def setTypeIcon(self):
        TaskType = self.getTaskType()

        # 绘制
        pixmap = QtGui.QPixmap(48, 48)
        pixmap.fill()
        painter = QtGui.QPainter(pixmap)

        if TaskType == '任务':
            painter.setBrush(QtGui.QColor('#0079bf'))
        elif TaskType == 'Story':
            painter.setBrush(QtGui.QColor('#61bd4f'))
        else:
            painter.setBrush(QtGui.QColor('#355263'))
        # painter.drawEllipse(0, 0, 48, 48) # 绘制圆
        painter.drawRoundedRect(0, 0, 47, 47, 15, 15) # 圆角矩形
        painter.end()
        
        label = self.label_TypeIcon
        # pixmap = QtGui.QPixmap(imgPath) # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        # pixmap = pixmap.scaled(48, 48)
        label.setPixmap(pixmap)  # 在label上显示图片
        label.setScaledContents(True) # 缩放像素图以填充可用空间,图片自适应label大小

    # ---------------- label_Detail_Img ----------------
    def setDetail_Img(self, imgPath):
        if not os.path.isfile(imgPath): # 判断文件
            imgPath = './UI/img_loss.png'
        print(imgPath)
        label = self.label_Detail_Img
        pixmap = QtGui.QPixmap(imgPath) # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        pixmap = pixmap.scaled(135, 85)
        label.setPixmap(pixmap)  # 在label上显示图片
        label.setAlignment(QtCore.Qt.AlignHCenter)
        label.setStyleSheet("border: 2px solid red") # 便于查看这个标签设置的大小范围
        label.setScaledContents(True) # 缩放像素图以填充可用空间,图片自适应label大小
        label.clicked.connect(lambda: self.on_Detail_Img_clicked(imgPath))

    def on_Detail_Img_clicked(self, imgPath):
        # label = self.sender()
        # 打开文件(可打开外部程序)
        sysstr = platform.system()
        if(sysstr =="Windows"):
            os.startfile(imgPath)
        elif(sysstr == "Linux"):
            subprocess.call(["xdg-open",imgPath])
        else:
            subprocess.call(["open", imgPath])
        

    # ---------------- FL_Info ----------------
    def setFL_Info(self, labels=[], datas=[], dataTypes=[]):
        labels = labels[8:]
        datas = datas[8:]
        dataTypes = dataTypes[8:]

        fromlayout = self.FL_Info
        for i in range(fromlayout.count()): 
            # fromlayout.itemAt(i).widget().delete()
            widgetItem = fromlayout.itemAt(0)
            if widgetItem != None:
                widget = widgetItem.widget()
                fromlayout.removeWidget(widget)
                widget.setParent(None)
                sip.delete(widget)
        for i in range(len(dataTypes)):
            label = QtWidgets.QLabel(labels[i])
            if dataTypes[i] == 'int':
                widght = QtWidgets.QSpinBox()
                widght.setFrame(False)
                widght.setFrame(False)
                widght.setMinimum(0)
                widght.setMaximum(1000)
                if datas[i] != '':
                    try:
                        widght.setValue(int(datas[i]))
                    except Exception as e:
                        widght.setValue(0)
                        print('setFL_Info error:%s' % (e))
                else:
                    widght.setValue(0)
            elif dataTypes[i] == 'float':
                widght = QtWidgets.QDoubleSpinBox()
                widght.setFrame(False)
                widght.setFrame(False)
                widght.setMinimum(0)
                widght.setMaximum(1000)
                if datas[i] != '':
                    try:
                        widght.setValue(float(datas[i]))
                    except Exception as e:
                        widght.setValue(0)
                        print('setFL_Info error:%s' % (e))
                else:
                    widght.setValue(0)
            elif dataTypes[i] == 'date':
                widght = QtWidgets.QDateEdit()
                widght.setDisplayFormat('yyyy-MM-dd')
                widght.setCalendarPopup(True)
                # widght.setMinimumWidth(180)
                if QtCore.QDate.fromString(datas[i], 'yyyy-MM-dd'):
                    widght.setDate(QtCore.QDate.fromString(datas[i], 'yyyy-MM-dd'))
                else:
                    now = QtCore.QDate.currentDate()  # 获取当前日期
                    widght.setDate(now)
            elif dataTypes[i] == 'longText':
                widght = QtWidgets.QTextEdit()
                widght.setMinimumSize(180, 85)
                widght.setText(datas[i])
            elif dataTypes[i].split(':')[0] == 'combo':
                combos = configure.get_DB_Struct(dataTypes[i].split(':')[1])
                widght = QtWidgets.QComboBox()
                # widght.setMinimumWidth(180)
                # 多个添加条目
                widght.addItems(combos)
                defaultComboId = int(dataTypes[i].split(':')[2])
                if dataTypes[i].split(':')[1] in combos:
                    defaultComboId = combos.index(dataTypes[i].split(':')[1])
                # 避免不是由用户引起的信号,因此我们使用blockSignals.
                widght.blockSignals(True)
                # ComboBox当前项使用setCurrentIndex()来设置
                widght.setCurrentIndex(defaultComboId)
                widght.blockSignals(False)
            else:
                widght = QtWidgets.QLineEdit()
                # widght.setMinimumWidth(180)
                widght.setText(datas[i])
            fromlayout.addRow(label, widght)
            # QtWidgets.QFormLayout.addRow()



# 自定义 Click label
class ClickLabel(QtWidgets.QLabel):

    clicked = QtCore.pyqtSignal()

    def __init__(self,parent = None):
        super(ClickLabel,self).__init__(parent)
        self.MyLabelPressed=0


    def mouseDoubleClickEvent(self, Event):
        print('label mouseDoubleClickEvent')


    def mousePressEvent(self,event):
        print 'mousePressEvent'
        self.clicked.emit()
        self.MyLabelPressed=1
 
    def mouseReleaseEvent(self,event):
        print 'mouseReleaseEvent'
        if self.MyLabelPressed==1:
            self.clicked.emit()
            self.MyLabelPressed=0
            QtGui.QLabel.mouseReleaseEvent(self, event)
