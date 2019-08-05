#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test.py
# @Author :  ()
# @Link   : 
# @Date   : 7/11/2019, 11:08:15 AM


import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class TreeItem(object):
    def __init__(self, data=[], parent=None):
        super(TreeItem, self).__init__()
        
        self._parentItem = parent
        self._childItems = []
        self._itemData = data

        if parent:
            parent.appendChild(self)

    def typeInfo(self):
        return "None"

    def appendChild(self, item):
        self._childItems.append(item)

    def insertChild(self, position, child):
        if position < 0 or position > len(self._childItems):
            return False
        
        self._childItems.insert(position, child)
        child._parentItem = self
        return True

    def removeChild(self, position):
        if position < 0 or position > len(self._childItems):
            return False

        child = self._childItems.pop(position)
        child._parentItem = None

    def child(self, row):
        return self._childItems[row]

    def childCount(self):
        return len(self._childItems)

    def columnCount(self):
        return len(self._itemData)

    def data(self, column):
        try:
            return self._itemData[column]
        except IndexError:
            return None

    def setData(self, value, column):
        self._itemData[column] = value

    def parent(self):
        return self._parentItem

    def row(self):
        if self._parentItem:
            return self._parentItem._childItems.index(self)

        return 0

    def log(self, tablevel=-1):
        output = '--'
        tablevel += 1
        
        for i in range(tablevel):
            output += "\t"

        output =output + "|------" + str(self._itemData) + "\n"

        for child in self._childItems:
            output =output + child.log(tablevel)

        tablevel -= 1
        return output

    def __repr__(self): # 返回一个可以用来表示对象的可打印字符串
        return self.log()


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)

        # 设置初始项的内容
        self._rootItem = data
        

    # 设置列数
    def columnCount(self, parent):
        return 9

    # 设置行数
    def rowCount(self, parent):
        # 当父项有效时，rowCount（）应返回0。
        if parent.column() > 0:
            return 0
        
        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    # 返回索引项目存储的数据。
    def data(self, index, role):
        if not index.isValid():
            return None

        # item = index.internalPointer()
        item = self.getItem(index)

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            # if index.column() == 1:
            return item.data(index.column())
            # elif index.column() == 2: 
            #     return item.typeInfo()

        # if role == QtCore.Qt.DecorationRole:
        #     if index.column() == 0:
        #         typeInfo = item.typeInfo()

        #         if typeInfo == "Camera":
        #             return QtGui.QIcon(QtGui.QPixmap('./UI/qt-logo.png'))

    # 返回一组标志
    def flags(self, index):

        # 复选框
        # if index.column() == 2:
        #     return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable

        # 基类实现返回一组标志，标志启用item（ItemIsEnabled），并允许它被选中（ItemIsSelectable）。
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    # 编辑数据
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            item = index.internalPointer()

            if role == QtCore.Qt.EditRole:
                # if index.column() == 1:
                item.setData(value, index.column())
                self.dataChanged.emit(index, index) # 更新Model的数据

                return True

        return False

    # 返回给定索引项的父级。如果项目没有父项，则返回无效的QModelIndex。
    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        item = index.internalPointer()
        parentItem = item.parent()

        if parentItem == self._rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    # 返回给定行、列和父索引指定的模型中，项的索引。
    def index(self, row, column, parent):
        # 索引不存在，返回无效索引
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        
        # 如果父项不存在，设置 parentItem = rootItem
        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        item = parentItem.child(row)
        if item:
            # 子类中重写此函数时，调用createIndex()以生成其他组件,用于项的模型索引。
            return self.createIndex(row, column, item)
        else:
            return QtCore.QModelIndex()

    # 设置标题行
    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if section == 0:
                return ""
            elif section == 1:
                return "任务"
            elif section == 2:
                return "类型"
            elif section == 3:
                return "状态"
            elif section == 4:
                return "执行人"
            elif section == 5:
                return "描述"
            elif section == 6:
                return "截止日期"
            elif section == 7:
                return "预估时间（小时）"
            elif section == 8:
                return "结余（小时）"
            else:
                return ""

        return None

    # 自定义函数，获取索引项
    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        
        return self._rootItem
  
    # 插入多列数据
    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1) # index, first, last
                
        for i in range(rows):
            childItem = TreeItem('insert item %d'%i)
            isSuccess = parentItem.insertChild(position, childItem)

        self.endInsertRows()

        return isSuccess
    
    # 删除多行数据（插入位置， 插入行数， 父项(默认父项为空项)）
    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        
        parentItem = self.getItem(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            isSuccess = parentItem.removeChild(position)

        self.endRemoveRows()

        return isSuccess


# Item class 部件
# 选择框
class ComboBoxDelegate_TaskType(QtWidgets.QItemDelegate):
    '''
    在应用它的列的每个单元格中放置一个功能齐全的QComboBox的委托
    '''
    # def __init__(self):
    #     QtWidgets.QItemDelegate.__init__(self)

    # createEditor 返回用于更改模型数据的小部件，可以重新实现以自定义编辑行为。
    def createEditor(self, parent, option, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItem('项目')
        editor.addItem('Story')
        editor.addItem('Epic')
        editor.addItem('任务')
        editor.addItem('里程碑')
        editor.addItem('信息')
        editor.addItem('文件夹')
        #多个添加条目
        editor.addItems(['功能','错误','改进','重构','研究','测试','文件'])
        #当下拉索引发生改变时发射信号触发绑定的事件
        editor.currentIndexChanged.connect(lambda:self.selectionchange(editor))

        return editor

    def selectionchange(self, editor):
        #currentText()：返回选中选项的文本
        ct = editor.currentText()
        print('Items in the list are:' + ct)

    # 设置编辑器从模型索引指定的数据模型项中显示和编辑的数据。
    def setEditorData(self, editor, index):
        data = index.model().data(index, QtCore.Qt.EditRole)
        comboId = 3
        if data == '项目':
            comboId = 0
        elif data == 'Story':
            comboId = 1
        elif data == 'Epic':
            comboId = 2
        elif data == '任务':
            comboId = 3
        elif data == '里程碑':
            comboId = 4
        elif data == '信息':
            comboId = 5
        elif data == '文件夹':
            comboId = 6
        elif data == '功能':
            comboId = 7
        elif data == '错误':
            comboId = 8
        elif data == '改进':
            comboId = 9
        elif data == '重构':
            comboId = 10
        elif data == '研究':
            comboId = 11
        elif data == '测试':
            comboId = 12
        elif data == '文件':
            comboId = 13

        # 避免不是由用户引起的信号,因此我们使用blockSignals.
        editor.blockSignals(True)
        # ComboBox当前项使用setCurrentIndex()来设置
        editor.setCurrentIndex(comboId) 
        editor.blockSignals(False)

    # 从编辑器窗口小部件获取数据，并将其存储在项索引处的指定模型中。
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)

    # 根据给定的样式选项更新索引指定的项目的编辑器。
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class ComboBoxDelegate_TaskState(ComboBoxDelegate_TaskType):
    # createEditor 返回用于更改模型数据的小部件，可以重新实现以自定义编辑行为。
    def createEditor(self, parent, option, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItem('待办')
        editor.addItem('进行中')
        editor.addItem('完成')
        #当下拉索引发生改变时发射信号触发绑定的事件
        editor.currentIndexChanged.connect(lambda:self.selectionchange(editor))

        return editor

    # 设置编辑器从模型索引指定的数据模型项中显示和编辑的数据。
    def setEditorData(self, editor, index):
        data = index.model().data(index, QtCore.Qt.EditRole)
        comboId = 0
        if data == '待办':
            comboId = 0
        elif data == '进行中':
            comboId = 1
        elif data == '完成':
            comboId = 2

        # 避免不是由用户引起的信号,因此我们使用blockSignals.
        editor.blockSignals(True)
        # ComboBox当前项使用setCurrentIndex()来设置
        editor.setCurrentIndex(comboId) 
        editor.blockSignals(False)

# 时间选择控件
class DateEditDelegate_TaskDeadline(QtWidgets.QItemDelegate):
    '''
    在应用它的列的每个单元格中放置一个功能齐全的QComboBox的委托
    '''
    # def __init__(self):
    #     QtWidgets.QItemDelegate.__init__(self)

    # self.dateEdit = QtGui.QDateEdit(QtCore.QDate.currentDate())
    # self.dateEdit.setDisplayFormat('yyyy-MM-dd')
    # self.dateEdit.setCalendarPopup(True)
    # createEditor 返回用于更改模型数据的小部件，可以重新实现以自定义编辑行为。
    def createEditor(self, parent, option, index):
        editor = QtWidgets.QDateEdit(parent)
        editor.setDisplayFormat('yyyy-MM-dd')
        editor.setCalendarPopup(True)

        return editor

    # 设置编辑器从模型索引指定的数据模型项中显示和编辑的数据。
    def setEditorData(self, editor, index):
        data = index.model().data(index, QtCore.Qt.EditRole)
        if QtCore.QDate.fromString(data, 'yyyy-MM-dd'):
            editor.setDate(QtCore.QDate.fromString(data, 'yyyy-MM-dd'))
        else:
            now = QtCore.QDate.currentDate()#获取当前日期
            editor.setDate(now)

    # 从编辑器窗口小部件获取数据，并将其存储在项索引处的指定模型中。
    def setModelData(self, editor, model, index):
        # current_Date = time.strftime("%Y-%m-%d", editor.date())
        current_Date = editor.date()
        print(current_Date.toString(QtCore.Qt.ISODate)) #ISO日期格式打印
        # print(current_Date.toString(Qt.DefaultLocaleLongDate)) #本地化长格式日期打印(2018年1月14日 )
        value = current_Date.toString(QtCore.Qt.ISODate)

        model.setData(index, value, QtCore.Qt.EditRole)

    # 根据给定的样式选项更新索引指定的项目的编辑器。
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


# 主界面
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)

        rootNode = TreeItem(['A', '1', '2', '3'])
        childNode1 = TreeItem(['A1', '1', '2', '3', '4', '5', 'None', '7', '8'], rootNode)
        childNode2 = TreeItem(['A2'], rootNode)
        childNode11 = TreeItem(['A21'], childNode1)
        childNode12 = TreeItem(['A21'], childNode1)
        childNode21 = TreeItem(['A21'], childNode2)
        childNode211 = TreeItem(['A21'], childNode21)

        print(rootNode)

        # 设置 Model
        self.model = TreeModel(rootNode)
        self.ui.treeView.setModel(self.model)

        # 设置 Item 部件
        self.TaskType = ComboBoxDelegate_TaskType()
        self.ui.treeView.setItemDelegateForColumn(2, self.TaskType)
        self.TaskState = ComboBoxDelegate_TaskState()
        self.ui.treeView.setItemDelegateForColumn(3, self.TaskState)
        self.TaskDeadline = DateEditDelegate_TaskDeadline()
        self.ui.treeView.setItemDelegateForColumn(6, self.TaskDeadline)
        # openPersistentEditor 显示组合框部件
        # self.ui.treeView.openPersistentEditor(self.model.index(0, 2,QtCore.QModelIndex()))

        # 切换选择事件
        self.ui.treeView.selectionModel().currentChanged.connect(self.setSelection)

    def setSelection(self, current, old):
        # openPersistentEditor 显示组合框部件
        # self.ui.treeView.openPersistentEditor(current.index(0, 2,current.parent()))
        pass


    def closeEvent(self, event):
        '''
        重写closeEvent方法
        '''
        event.accept()
        quit()


if __name__ == '__main__':
    
    # app = None
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow('./UI/test.ui')
    w.show()

    sys.exit(app.exec_())