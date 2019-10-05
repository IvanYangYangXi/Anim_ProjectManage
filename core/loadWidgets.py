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
import threading, time
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


# 任务面板 树列表 对应的 详细信息面板UI
class DetailPage(QtWidgets.QWidget):
    def __init__(self, uiPath='', parent=None):
        super(DetailPage, self).__init__(parent)

        if uiPath == '':
            uiPath = './UI/Widget_DetailPage.ui'
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)

        self.datas = [] # Item 数据
        self.thread_imgBtn = None # 按钮计时器线程
        self.model_Proj_Task = None # 任务面板 树列表 对应的 Model
        self.currentIndex = None # 当前选择的 Index

        # 关闭按钮 点击事件
        self.closeButton = self.ui.pushButton_Detail_Close
        self.closeButton.setToolTip('关闭详细面板')
        self.closeButton.clicked.connect(self.closeEvent)

        # name
        # self.ui.lineEdit_TaskName.textChanged.connect(self.nameChanged) # 当内容改变时触发事件
        self.ui.lineEdit_TaskName.editingFinished.connect(lambda: self.lineEditFinished(self.ui.lineEdit_TaskName, u'任务')) # 当内容修改完成时触发事件

        # Type
        self.comboBox_TaskType = self.ui.comboBox_TaskType
        taskType = configure.get_DB_Struct('TaskType')
        # 添加多个添加条目
        self.comboBox_TaskType.addItems(taskType)
        # 当下拉索引发生改变时发射信号触发绑定的事件
        self.comboBox_TaskType.currentIndexChanged.connect(
            lambda: self.comboBoxSelectionChanged(self.comboBox_TaskType, u'类型'))

        # State
        self.comboBox_TaskState = self.ui.comboBox_TaskState
        TaskState = configure.get_DB_Struct('TaskState')
        # 添加多个添加条目
        self.comboBox_TaskState.addItems(TaskState)
        # # 当下拉索引发生改变时发射信号触发绑定的事件
        self.comboBox_TaskState.currentIndexChanged.connect(
            lambda: self.comboBoxSelectionChanged(self.comboBox_TaskState, u'状态'))

        # TreePath
        self.HL_Detail_TreePath = self.ui.horizontalLayout_Detail_TreePath

        # TypeIcon
        self.label_TypeIcon = self.ui.label_TypeIcon

        # Detail_Img
        # QtWidgets.QHBoxLayout.replaceWidget()
        self.Detail_Img = self.ui.pushButton_Detail_Img
        self.imgPath = os.path.abspath('./UI/img_loss.png')
        self.Detail_Img.clicked.connect(self.on_Detail_Img_clicked) 
        self.BtnTime = 0 # 用于防止过快的重复点击
        # 重设右键并绑定信号槽
        self.Detail_Img.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.Detail_Img.customContextMenuRequested[QtCore.QPoint].connect(self.Detail_ImgContext)

        # -------- Info ---------
        self.FL_Info = self.ui.formLayout_Detail_Info
        self.widght = [] # 用于存储动态添加的部件


    # 应用详细面板修改的内容
    def dataChanged(self, label, data):
        labels = configure.get_DB_Struct("rootNode_taskInfo")
        # print(label,labels)
        if label in labels:
            num = labels.index(label)
            if self.model_Proj_Task != None:
                self.model_Proj_Task.setDataByDetail(self.model_Proj_Task.getColumnIndex(self.currentIndex, num-4), data)
    
    # 关闭事件
    def closeEvent(self):

        # 将其父设置为空，隐藏控件
        self.setParent(None)

    # 自定义 Detail_Img 右键按钮
    def Detail_ImgContext(self):
        popMenu = QtWidgets.QMenu()
        popMenu.addAction(QtWidgets.QAction(u'设置缩略图', self))
        popMenu.addAction(QtWidgets.QAction(u'清除缩略图', self))
        popMenu.triggered[QtWidgets.QAction].connect(self.processtrigger)
        popMenu.exec_(Qt.QCursor.pos())
    
    # Detail_Img 右键按钮事件
    def processtrigger(self, q):
        # 输出那个Qmenu对象被点击
        if q.text().encode("utf-8") == "设置缩略图":
            filePath = configure.getProjectPath() + '/data/Content/%s'%(self.datas[0])
            if not os.path.exists(filePath):
                os.makedirs(filePath) # 创建路径
            imgPath = QtWidgets.QFileDialog.getOpenFileName(None, "Find Img", \
                filePath, "Image Files(*.jpg *.png *.jpge *.tga *.gif)")
            self.imgPath = imgPath[0]
            self.setDetail_Img(self.imgPath)
            # set 任务树item的缩略图
            self.dataChanged(u'缩略图', self.imgPath)
        elif q.text().encode("utf-8") == "清除缩略图":
            self.setDetail_Img()
            # set 任务树item的缩略图
            self.dataChanged(u'缩略图', self.imgPath)

    # -------------- 内容改变时 -----------------
    # lineEdit
    def lineEditFinished(self, editor, label):
        # 检测是否进行了任何更改
        if editor.isModified(): 
            self.dataChanged(label, editor.text())
        editor.setModified(False)

    # lineEdit
    def textEditFinished(self, editor, label):
        # QtWidgets.QTextEdit.toPlainText
        print(editor, label)
        self.dataChanged(label, editor.toPlainText())

    # spinBox
    def spinBoxFinished(self, editor, label):
        # QtWidgets.QSpinBox.value
        self.dataChanged(label, editor.value())

    # QtWidgets.QDateEdit
    def dateEditFinished(self, editor, label):
        # QtWidgets.QDateEdit.date
        self.dataChanged(label, editor.date())

    # comboBox
    def comboBoxSelectionChanged(self, editor, label):
        # currentText()：返回选中选项的文本
        ct = editor.currentText()
        self.dataChanged(label, ct)

    # -------------- Name -----------------
    # set name
    def setTaskName(self, data):
        self.ui.lineEdit_TaskName.setText(data)

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
            lable.setText(u" <a href='none' style='color:blue'>%s</a>"%i)
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

        if TaskType.encode("utf-8") == '任务':
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

    # ---------------- Detail_Img ----------------
    def setDetail_Img(self, imgPath=''):
        if os.path.isfile(os.path.abspath(imgPath)): # 判断文件
            self.imgPath = os.path.abspath(imgPath)
        else:
            self.imgPath = os.path.abspath('./UI/img_loss.png')
        # print(self.imgPath)
        button = self.Detail_Img
        pixmap = QtGui.QPixmap(self.imgPath) # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        pixmap = pixmap.scaled(135, 85)
        icon = QtGui.QIcon(pixmap)
        button.setIcon(icon)  # 在button上显示图片
        button.setIconSize(QtCore.QSize(135, 85))
        # label.setAlignment(QtCore.Qt.AlignHCenter)
        # label.setStyleSheet("border: 2px solid red") # 便于查看这个标签设置的大小范围
        # label.setScaledContents(True) # 缩放像素图以填充可用空间,图片自适应label大小

    def on_Detail_Img_clicked(self):
        # label = self.sender()
        if self.thread_imgBtn != None: # 判断上一线程是否存在
            if self.thread_imgBtn.is_alive(): # 判断上一线程是否在运行
                print('alive')
                return None
        if self.BtnTime == 0:
            self.BtnTime = 1
            self.openFile(self.imgPath)
        thread_imgBtn = threading.Thread(target=self.timeing) # 新建计时线程
        self.thread_imgBtn = thread_imgBtn
        thread_imgBtn.setDaemon(True) # 设置子线程为守护线程时，主线程一旦执行结束，则全部线程全部被终止执行
        thread_imgBtn.start()
        
    def openFile(self, path):
        if path == os.path.abspath('./UI/img_loss.png'):
            filePath = configure.getProjectPath() + '/data/Content/%s'%(self.datas[0])
            if not os.path.exists(filePath):
                os.makedirs(filePath) # 创建路径
            imgPath = QtWidgets.QFileDialog.getOpenFileName(None, "Find Img", \
                filePath, "Image Files(*.jpg *.png *.jpge *.tga *.gif)")
            self.imgPath = imgPath[0]
            self.setDetail_Img(imgPath[0])
            # set 任务树item的缩略图
            self.dataChanged(u'缩略图', self.imgPath)
        else:
            # 打开文件(可打开外部程序)
            sysstr = platform.system()
            if(sysstr =="Windows"):
                # print('Windows')
                os.startfile(path)
            elif(sysstr == "Linux"):
                # print('Linux')
                subprocess.call(["xdg-open", path])
            else:
                # print('otherSys')
                subprocess.call(["open", path])

    # 计时器
    def timeing(self):
        time.sleep(1) # 防止过快的重复点击
        self.BtnTime = 0

    # ---------------- FL_Info ----------------
    def setFL_Info(self, labels=[], datas=[], dataTypes=[]):
        labels = labels[8:]
        datas = datas[8:]
        dataTypes = dataTypes[8:]

        self.widght = range(len(dataTypes))

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
                self.widght[i] = QtWidgets.QSpinBox()
                self.widght[i].setFrame(False)
                self.widght[i].setFrame(False)
                self.widght[i].setMinimum(0)
                self.widght[i].setMaximum(1000)
                if datas[i] != '':
                    try:
                        self.widght[i].setValue(int(datas[i]))
                    except Exception as e:
                        self.widght[i].setValue(0)
                        print('setFL_Info error:%s' % (e))
                else:
                    self.widght[i].setValue(0)
                # 当内容修改完成时触发事件
                self.widght[i].editingFinished.connect(lambda: self.spinBoxFinished(self.widght[i], labels[i]))
            elif dataTypes[i] == 'float':
                self.widght[i] = QtWidgets.QDoubleSpinBox()
                self.widght[i].setFrame(False)
                self.widght[i].setFrame(False)
                self.widght[i].setMinimum(0)
                self.widght[i].setMaximum(1000)
                if datas[i] != '':
                    try:
                        self.widght[i].setValue(float(datas[i]))
                    except Exception as e:
                        self.widght[i].setValue(0)
                        print('setFL_Info error:%s' % (e))
                else:
                    self.widght[i].setValue(0)
                # 当内容修改完成时触发事件
                self.widght[i].editingFinished.connect(lambda: self.spinBoxFinished(self.widght[i], labels[i]))
            elif dataTypes[i] == 'date':
                self.widght[i] = QtWidgets.QDateEdit()
                self.widght[i].setDisplayFormat('yyyy-MM-dd')
                self.widght[i].setCalendarPopup(True)
                # self.widght[i].setMinimumWidth(180)
                if QtCore.QDate.fromString(datas[i], 'yyyy-MM-dd'):
                    self.widght[i].setDate(QtCore.QDate.fromString(datas[i], 'yyyy-MM-dd'))
                else:
                    now = QtCore.QDate.currentDate()  # 获取当前日期
                    self.widght[i].setDate(now)
                # 当内容修改完成时触发事件
                self.widght[i].editingFinished.connect(lambda: self.dateEditFinished(self.widght[i], labels[i]))
            elif dataTypes[i] == 'longText':
                self.widght[i] = CustomTextEdit()
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) 
                sizePolicy.setHorizontalStretch(0) 
                sizePolicy.setVerticalStretch(0) 
                self.widght[i].setSizePolicy(sizePolicy)
                self.widght[i].setMinimumSize(180, 50)
                self.widght[i].setMaximumHeight(85)
                self.widght[i].setText(datas[i])
                # 当内容修改完成时触发事件
                # self.widght[i].focus_out(self.textEditFinished(self.widght[i], labels[i]))
                self.widght[i].focus_out.connect(lambda: self.textEditFinished(self.widght[i], labels[i]))
            elif dataTypes[i].split(':')[0] == 'combo':
                combos = configure.get_DB_Struct(dataTypes[i].split(':')[1])
                self.widght[i] = QtWidgets.QComboBox()
                # self.widght[i].setMinimumWidth(180)
                # 多个添加条目
                self.widght[i].addItems(combos)
                defaultComboId = int(dataTypes[i].split(':')[2])
                if datas[i] in combos:
                    defaultComboId = combos.index(datas[i])
                # 避免不是由用户引起的信号,因此我们使用blockSignals.
                self.widght[i].blockSignals(True)
                # ComboBox当前项使用setCurrentIndex()来设置
                self.widght[i].setCurrentIndex(defaultComboId)
                self.widght[i].blockSignals(False)
                # 当内容修改完成时触发事件
                self.widght[i].currentIndexChanged.connect(lambda: self.comboBoxSelectionChanged(self.widght[i], labels[i]))
            elif dataTypes[i] == 'text' or dataTypes[i] == 'personnel':
                self.widght[i] = QtWidgets.QLineEdit()
                # self.widght[i].setMinimumWidth(180)
                self.widght[i].setText(datas[i])
                # 当内容修改完成时触发事件
                # print(self.widght[i])
                self.widght[i].editingFinished.connect(lambda: self.lineEditFinished(self.widght[i], labels[i]))
            fromlayout.addRow(label, self.widght[i])
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


# 自定义 TextEdit
class CustomTextEdit(QtWidgets.QTextEdit):

    focus_out = QtCore.pyqtSignal()

    def __init__(self):
        super(CustomTextEdit,self).__init__()

    def focusOutEvent(self, event):
        super(CustomTextEdit,self).focusOutEvent(event)
        self.focus_out.emit()