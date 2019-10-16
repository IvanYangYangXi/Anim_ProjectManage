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
import win32con, win32api
import configure
import shutil # 文件夹操作


# 项目列表项
class ListItem_General_Proj(QtWidgets.QWidget):
    def __init__(self, uiPath='', parent=None):
        super(ListItem_General_Proj, self).__init__(parent)

        if uiPath == '':
            uiPath = './UI/listItem_General_Proj.ui'
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)


# 细节面板文件列表项
class ListItem_fileItem(QtWidgets.QWidget):
    def __init__(self, uiPath='', parent=None):
        super(ListItem_fileItem, self).__init__(parent)

        if uiPath == '':
            uiPath = './UI/listItem_fileItem.ui'
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
        self.ui.pushButton_V_Detail_Close.clicked.connect(self.closeEvent) # 侧边关闭按钮

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

        # -------- fileList ---------
        self.fileList = DropListWidget()
        self.ui.verticalLayout_file.addWidget(self.fileList)
        self.fileList.datas = self.datas # 更新文件列表对应的items数据


    # 应用详细面板固定项修改的内容
    def dataChanged(self, label, data):
        labels = configure.get_DB_Struct("rootNode_taskInfo")
        # print(label,labels)
        if label in labels:
            num = labels.index(label)
            if self.model_Proj_Task != None:
                self.model_Proj_Task.setDataByDetail(self.model_Proj_Task.getColumnIndex(self.currentIndex, num-4), data)
    
    # 应用详细面板动态项修改的内容
    def dataChangedAll(self):
        # labels = configure.get_DB_Struct("rootNode_taskInfo")
        if self.datas != []:
            # print(self.datas)
            x = 7
            for i in self.widght:
                x += 1
                if i.inherits('QSpinBox'):
                    self.datas[x] = i.value()
                elif i.inherits('QDoubleSpinBox'):
                    self.datas[x] = i.value()
                elif i.inherits('QDateEdit'):
                    self.datas[x] = i.date().toString(QtCore.Qt.ISODate) # 获取日期并转化为文字
                elif i.inherits('QTextEdit'):
                    self.datas[x] = i.toPlainText()
                elif i.inherits('QComboBox'):
                    self.datas[x] = i.currentText()
                elif i.inherits('QLineEdit'):
                    self.datas[x] = i.text()
                else:
                    print('FL_Info 存在未指定的控件类型')
            if self.model_Proj_Task != None:
                self.model_Proj_Task.setAllDatasByDetail(self.model_Proj_Task.getColumnIndex(self.currentIndex, 0), self.datas)
                self.fileList.datas = self.datas
    
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
            # 选择缩略图
            imgPath = QtWidgets.QFileDialog.getOpenFileName(None, "Find Img", \
                filePath, "Image Files(*.jpg *.png *.jpge *.tga *.gif)")
            # 设置缩略图
            if imgPath[1]:
                imgName = os.path.split(imgPath[0])[1] # 分离文件名
                if not os.path.exists(filePath+'/$PMF_SystemFiles'):
                    os.makedirs(filePath+'/$PMF_SystemFiles') # 创建系统文件路径
                    if 'Windows' in platform.system():
                        win32api.SetFileAttributes(filePath+'/$PMF_SystemFiles', win32con.FILE_ATTRIBUTE_HIDDEN) # 隐藏文件夹
                if os.path.exists(filePath+'/$PMF_SystemFiles'+imgName):
                    os.remove(filePath+'/$PMF_SystemFiles'+imgName)
                shutil.copy(imgPath[0], filePath+'/$PMF_SystemFiles') # 复制文件到指定目录
                imgRelativePath = '/data/Content/%s'%(self.datas[0]) + '/$PMF_SystemFiles/' + imgName # 重组路径,相对路径
                self.imgPath = configure.getProjectPath() + imgRelativePath
                self.setDetail_Img(self.imgPath)
                # set 任务树item的缩略图
                self.dataChanged(u'缩略图', imgRelativePath)
        elif q.text().encode("utf-8") == "清除缩略图":
            self.setDetail_Img()
            # set 任务树item的缩略图
            self.dataChanged(u'缩略图', '')

    # -------------- 内容改变时 -----------------
    # lineEdit
    def lineEditFinished(self, editor, label):
        # 检测是否进行了任何更改
        if editor.isModified(): 
            self.dataChanged(label, editor.text())
        editor.setModified(False)

    # textEdit
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
        self.datas[4] = data
        self.fileList.datas = self.datas

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

            self.datas[6] = data
            self.fileList.datas = self.datas

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
            self.datas[7] = data
            self.fileList.datas = self.datas

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
        if path == os.path.abspath('./UI/img_loss.png') or os.path.isfile():
            filePath = configure.getProjectPath() + '/data/Content/%s'%(self.datas[0])
            if not os.path.exists(filePath):
                os.makedirs(filePath) # 创建路径
            # 选择缩略图
            imgPath = QtWidgets.QFileDialog.getOpenFileName(None, "Find Img", \
                filePath, "Image Files(*.jpg *.png *.jpge *.tga *.gif)")
            # 设置缩略图
            if imgPath[1]:
                imgName = os.path.split(imgPath[0])[1] # 分离文件名
                if not os.path.exists(filePath+'/$PMF_SystemFiles'):
                    os.makedirs(filePath+'/$PMF_SystemFiles') # 创建系统文件路径
                    if 'Windows' in platform.system():
                        win32api.SetFileAttributes(filePath+'/$PMF_SystemFiles', win32con.FILE_ATTRIBUTE_HIDDEN) # 隐藏文件夹
                if os.path.exists(filePath+'/$PMF_SystemFiles'+imgName):
                    os.remove(filePath+'/$PMF_SystemFiles'+imgName)
                shutil.copy(imgPath[0], filePath+'/$PMF_SystemFiles') # 复制文件到指定目录
                imgRelativePath = '/data/Content/%s'%(self.datas[0]) + '/$PMF_SystemFiles/' + imgName # 重组路径,相对路径
                self.imgPath = configure.getProjectPath() + imgRelativePath
                self.setDetail_Img(self.imgPath)
                # set 任务树item的缩略图
                self.dataChanged(u'缩略图', imgRelativePath)
        else:
            path = os.path.abspath(path)
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
        # 清理FL_Info
        for i in range(fromlayout.count()): 
            # fromlayout.itemAt(i).widget().delete()
            widgetItem = fromlayout.itemAt(0)
            if widgetItem != None:
                widget = widgetItem.widget()
                fromlayout.removeWidget(widget)
                widget.setParent(None)
                sip.delete(widget)
        # 添加控件
        for i in range(len(dataTypes)):
            label = QtWidgets.QLabel(labels[i])
            if dataTypes[i] == 'text' or dataTypes[i] == 'personnel':
                self.widght[i] = QtWidgets.QLineEdit()
                # self.widght[i].setMinimumWidth(180)
                self.widght[i].setText(datas[i])
                # 当内容修改完成时触发事件
                self.widght[i].editingFinished.connect(self.dataChangedAll)
            elif dataTypes[i] == 'string':
                self.widght[i] = QtWidgets.QLineEdit()
                # self.widght[i].setMinimumWidth(180)
                self._mask = QtCore.QRegExp("[0-9A-Za-z_-]{49}") # 为给定的模式字符串构造一个正则表达式对象。(字符只能是字母或者数字或下划线,长度不能超过50位)
                validator = QtGui.QRegExpValidator(self._mask, self.widght[i]) # 构造一个验证器，该父对象接受与正则表达式匹配的所有字符串。这里的父对象就是QLineEdit对象了。
                self.widght[i].setValidator(validator) #将密码输入框设置为仅接受符合验证器条件的输入。 这允许您对可能输入的文本设置任何约束条件。
                self.widght[i].setText(datas[i])
                # 当内容修改完成时触发事件
                self.widght[i].editingFinished.connect(self.dataChangedAll)
            elif dataTypes[i] == 'int':
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
                self.widght[i].editingFinished.connect(self.dataChangedAll)
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
                self.widght[i].editingFinished.connect(self.dataChangedAll)
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
                self.widght[i].editingFinished.connect(self.dataChangedAll)
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
                self.widght[i].focus_out.connect(self.dataChangedAll)
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
                self.widght[i].currentIndexChanged.connect(self.dataChangedAll)
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


# ------------ 列表 -------------------#
class DropListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(DropListWidget, self).__init__(parent)

        self.lastPath = configure.getProjectPath()
        self.datas = [] # Item 数据

        self.setAcceptDrops(True)
        self.setDragEnabled(True) # 开启可拖放事件
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection) # 按住CTRL可多选
        # 创建右键菜单
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showListRightMenu)
        # 双击打开文件
        self.itemDoubleClicked.connect(self.openFile)
        # 设置自定义item
        # self.item = QtWidgets.QListWidgetItem()  # 创建QListWidgetItem对象
        # self.item.setSizeHint(QtCore.QSize(200, 50))  # 设置QListWidgetItem大小
        # self.itemWidget = ListItem_fileItem()  # itemWidget
        # self.addItem(self.item)  # 添加item
        # self.setItemWidget(self.item, self.itemWidget)  # 为item设置widget

        self._path = '' # 列表显示内容所在目录
        # 显示的列表
        self.showSource = True
        self.showMesh = True
        self.showTex = True
        self.showRevisions = False
        self.prefix = ['SM_', 'T_'] # 默认前缀
        self.suffix = ['', ''] # 默认后缀

    # 拖放进入事件
    def dragEnterEvent(self, event):
        print(event.mimeData().urls())  # 文件所有的路径
        print(event.mimeData().text())  # 文件路径
        # print(event.mimeData().formats())  # 支持的所有格式
        if self._path != '':
            if event.mimeData().hasUrls():
                event.accept()
            elif event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
                items = self.selectedItems()
                urls = []
                for i in items:
                    urls.append(QtCore.QUrl('file:///' + os.path.join(self._path, i.text())))
                event.mimeData().setUrls(urls)
                event.accept()
            else:
                event.ignore()
        else:
            showErrorMsg('请先选择目录')
            event.ignore()

    # 拖放移动事件
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        elif event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    # 拖放释放事件
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            pathes = event.mimeData().urls()
            for path in pathes:
                s = str(path)
                s = s.replace("PyQt5.QtCore.QUrl('file:///",'')
                s = s.replace("PyQt5.QtCore.QUrl(u'file:///",'')
                s = s.replace("')", '')
                print(s)
                if os.path.isfile(s):
                    fpath,fname = os.path.split(s) # 分离文件名和路径
                    # fname = os.path.split(s)[1] # 获取文件名带后缀
                    meshPath = self._path + '/Content/Meshes'
                    texPath = self._path + '/Content/Textures'
                    sourceFilePath = self._path + '/Content/SourceFile'

                    # 模型文件
                    # os.path.splitext(s)[1] # 获取文件后缀
                    if os.path.splitext(s)[1] in ['.fbx', '.abc', '.FBX', '.ABC', '.obj', '.OBJ']:
                        # 重命名
                        if self.datas[configure.getIndexByLabel(u'英文简称')] != '':
                            abbreviation = self.datas[configure.getIndexByLabel(u'英文简称')] # 获取英文简称
                        else:
                            abbreviation = os.path.splitext(fname)[0]
                        newFName = self.prefix[0] + abbreviation + self.suffix[0] + os.path.splitext(s)[1] # 重组名字
                        if fname != newFName:
                            text, ok=QtWidgets.QInputDialog.getText(self, '重命名', '重命名：', QtWidgets.QLineEdit.Normal, "%s"%(newFName))
                            if ok and text:
                                newFName = text
                            else:
                                newFName = fname
                        # 历史版本
                        if os.path.isfile(meshPath+'/'+newFName): # 文件是否已存在（重名文件）
                            if not os.path.exists(meshPath + '/Revisions'): # 历史版本文件夹
                                os.makedirs(meshPath + '/Revisions') # 创建路径
                            # 移动文件到历史版本文件夹,并重命名及记录版本创建时间
                            ftime = time.strftime('%y%m%d%H%M%S',time.localtime(time.time()))
                            shutil.move(meshPath+'/'+newFName, meshPath+'/Revisions/'+os.path.splitext(newFName)[0]+'_'+ftime+os.path.splitext(s)[1]) 
                        # 复制文件
                        if not os.path.exists(meshPath):
                            os.makedirs(meshPath) # 创建路径
                        shutil.copy(s, meshPath) # 复制文件
                    # 贴图文件
                    elif os.path.splitext(s)[1] in ['.tga', '.TGA', '.jpg', '.jpeg', '.png', '.dds']:
                        # 重命名
                        newFName = self.prefix[1] + abbreviation + self.suffix[1] + os.path.splitext(s)[1]
                        if fname != newFName:
                            text, ok=QtWidgets.QInputDialog.getText(self, '重命名', '重命名：', QtWidgets.QLineEdit.Normal, "%s"%(newFName))
                            if ok and text:
                                newFName = text
                            else:
                                newFName = fname
                        # 历史版本
                        if os.path.isfile(texPath+'/'+newFName): # 文件是否已存在（重名文件）
                            if not os.path.exists(texPath + '/Revisions'): # 历史版本文件夹
                                os.makedirs(texPath + '/Revisions') # 创建路径
                            # 移动文件到历史版本文件夹,并重命名及记录版本创建时间
                            ftime = time.strftime('%y%m%d%H%M%S',time.localtime(time.time()))
                            shutil.move(texPath+'/'+newFName, texPath+'/Revisions/'+os.path.splitext(newFName)[0]+'_'+ftime+os.path.splitext(s)[1]) 
                        # 复制文件
                        if not os.path.exists(texPath):
                            os.makedirs(texPath) # 创建路径
                        shutil.copy(s, texPath) # 复制文件
                    # 源文件（其他文件）
                    else:
                        # 重命名
                        if os.path.splitext(s)[1] in ['.mb', '.ma', '.max', '.ZBR', '.zbr', '.ZTL', '.ztl']:
                            newFName = self.prefix[0] + abbreviation + self.suffix[0] + os.path.splitext(s)[1]
                        else:
                            newFName = abbreviation + self.suffix[0] + os.path.splitext(s)[1]
                        if fname != newFName:
                            text, ok=QtWidgets.QInputDialog.getText(self, '重命名', '重命名：', QtWidgets.QLineEdit.Normal, "%s"%(newFName))
                            if ok and text:
                                newFName = text
                            else:
                                newFName = fname
                        # 历史版本
                        if os.path.isfile(sourceFilePath+'/'+newFName): # 文件是否已存在（重名文件）
                            if not os.path.exists(sourceFilePath + '/Revisions'): # 历史版本文件夹
                                os.makedirs(sourceFilePath + '/Revisions') # 创建路径
                            # 移动文件到历史版本文件夹,并重命名及记录版本创建时间
                            ftime = time.strftime('%y%m%d%H%M%S',time.localtime(time.time()))
                            shutil.move(sourceFilePath+'/'+newFName, sourceFilePath+'/Revisions/'+os.path.splitext(newFName)[0]+'_'+ftime+os.path.splitext(s)[1]) 
                        # 复制文件
                        if not os.path.exists(sourceFilePath):
                            os.makedirs(sourceFilePath) # 创建路径
                        shutil.copy(s, sourceFilePath) # 复制文件
            self.updateList()

    # 更新文件列表
    def updateList(self):
        meshPath = self._path + '/Content/Meshes'
        texPath = self._path + '/Content/Textures'
        sourceFilePath = self._path + '/Content/SourceFile'

        # 设置自定义item
        # item = QtWidgets.QListWidgetItem()  # 创建QListWidgetItem对象
        # item.setSizeHint(QtCore.QSize(200, 50))  # 设置QListWidgetItem大小
        # itemWidget = ListItem_fileItem()  # itemWidget
        # self.addItem(item)  # 添加item
        # self.setItemWidget(item, itemWidget)  # 为item设置widget

        self.clear()
        if self.showSource:
            if os.path.exists(sourceFilePath):
                for data in os.listdir(sourceFilePath): # 获取当前路径下的文件
                    self.addItem(data)
        if self.showMesh:
            if os.path.exists(meshPath):
                for data in os.listdir(meshPath): # 获取当前路径下的文件
                    self.addItem(data)
        if self.showTex:
            if os.path.exists(texPath):
                for data in os.listdir(texPath): # 获取当前路径下的文件
                    self.addItem(data)
        # 历史文件
        if self.showRevisions:
            if self.showSource:
                if os.path.exists(sourceFilePath + '/Revisions'):
                    for data in os.listdir(sourceFilePath + '/Revisions'): 
                        self.addItem(data)
            if self.showMesh:
                if os.path.exists(meshPath + '/Revisions'):
                    for data in os.listdir(meshPath + '/Revisions'): 
                        self.addItem(data)
            if self.showTex:
                if os.path.exists(texPath + '/Revisions'):
                    for data in os.listdir(texPath + '/Revisions'): 
                        self.addItem(data)

    # 创建右键菜单(list)
    def showListRightMenu(self, pos):
        # 创建QMenu
        rightMenu = QtWidgets.QMenu(self)
        itemOpen = rightMenu.addAction('打开路径')
        itemImport = rightMenu.addAction('导入文件')
        itemRefresh = rightMenu.addAction('刷新')
        rightMenu.addSeparator() # 分隔器
        accessories = rightMenu.addAction('设置缩略图')
        cleraAccessories = rightMenu.addAction('清除缩略图')
        itemRename = rightMenu.addAction('重命名')
        # itemAddChild = rightMenu.addAction('添加子项')
        itemDelete = rightMenu.addAction('删除选择项')
        rightMenu.addSeparator() # 分隔器
        # item3.setEnabled(False)
        # # 添加二级菜单
        # secondMenu = rightMenu.addMenu('二级菜单')
        # item4 = secondMenu.addAction('test4')

        items = self.selectedItems()
        # 禁用项
        if len(items) != 1:
            itemRename.setEnabled(False)
            accessories.setEnabled(False)
            cleraAccessories.setEnabled(False)
        if len(items) == 0:
            itemDelete.setEnabled(False)
        # 将动作与处理函数相关联 
        # item1.triggered.connect()

        action = rightMenu.exec_(QtGui.QCursor.pos()) # 在鼠标位置显示
        # ------------------ 右键事件 ------------------- #
        if action == itemImport:
            if self._path != '':
                files = QtWidgets.QFileDialog.getOpenfnames(None, "Find File", self.lastPath)[0] # 选择文件
                self.lastPath = os.path.split(files[0])[0] # 设置选择文件的目录
                for path in files:
                    if os.path.isfile(path):
                        if not os.path.exists(self._path):
                            os.makedirs(self._path) # 创建路径
                        shutil.copy(path, self._path) # 复制文件
                self.updateList()
            else:
                showErrorMsg('请先选择目录')
        # 打开路径（在资源管理器中显示）
        if action == itemOpen:
            if os.path.exists(self._path):
                os.startfile(self._path)
        # 刷新
        if action == itemRefresh:
            self.updateList()
        # 重命名
        if action == itemRename:
            value, ok = QtWidgets.QInputDialog.getText(self, "重命名", "请输入文本:", QtWidgets.QLineEdit.Normal, os.path.splitext(items[0].text())[0])
            if ok:
                try:
                    os.rename(os.path.join(self._path, items[0].text()), os.path.join(self._path, value + os.path.splitext(items[0].text())[1]))
                    self.updateList()
                except Exception as e:
                    showErrorMsg('重命名失败，错误代码：%s'%(e))
        # 删除选择项
        if action == itemDelete:
            reply = QtWidgets.QMessageBox.warning(self, "消息框标题",  "确认删除选择项?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply:
                for i in items:
                    path = os.path.join(self._path, i.text())
                    os.remove(path)    #删除文件
                self.updateList()
        
    # 打开文件(可打开外部程序)
    def openFile(self, item):
        os.startfile(os.path.join(self._path, item.text()))


# # ---------- 文件列表 ----------- #
# class DetailFileListWidget(DropListWidget):



def showErrorMsg(msg):
    print(msg)