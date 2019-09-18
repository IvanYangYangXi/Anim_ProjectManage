#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# treeModels.py
# @Author :  ()
# @Link   :
# @Date   : 7/10/2019, 2:58:31 PM


import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import DB
import configure


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

    def datas(self):
        return self._itemData

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

        output = output + "|------" + str(self._itemData) + "\n"

        for child in self._childItems:
            output = output + child.log(tablevel)

        tablevel -= 1
        return output

    def __repr__(self):  # 返回一个可以用来表示对象的可打印字符串
        return self.log()


class BaseTreeItem(TreeItem):
    def __init__(self, data=[], parent=None):
        super(BaseTreeItem, self).__init__()

        self._parentItem = parent
        self._childItems = []
        self._itemData = list(data) # 将元组转换为列表
        self._dbId = self._itemData[0]

        if parent:
            parent.appendChild(self)

    def columnCount(self):
        return len(self._itemData) - 4

    def data(self, column):
        try:
            return self._itemData[column + 4]
        except IndexError:
            return None

    def setData(self, value, column):
        # self._itemData = list(self._itemData) # 将元组转换为列表
        # print(self._itemData)
        self._itemData[column + 4] = value

        # 更新数据库数据
        dbKey = configure.get_DB_Struct('struct_taskInfo')[column + 3]
        DB.updateData(configure.getProjectPath(), 'table_taskInfo', 'id=%d' %
                      (self._dbId), '%s="%s"' % (dbKey, value))


# ----------------------------- TreeModel -------------------------------- #
class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, item, parent=None):
        super(TreeModel, self).__init__(parent)

        # 设置初始项的item
        # self._rootItem = TreeItem(data)
        self._rootItem = item

    # 设置列数
    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self._rootItem.columnCount()

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
                self.dataChanged.emit(index, index)  # 更新Model的数据

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
            return QtCore.QVariant(self._rootItem.data(section))

        return None

    # 自定义函数，获取索引项
    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self._rootItem

    # 插入多行数据
    def insertRows(self, position, rows, parent=QtCore.QModelIndex(), items=[]):

        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position +
                             rows - 1)  # index, first, last
        isSuccess = False
        for i in range(rows):
            childItem = items[i]
            isSuccess = parentItem.insertChild(position, childItem)
            print(childItem.datas())

        self.endInsertRows()
        
        return isSuccess

    # 删除多行数据（插入位置， 插入行数， 父项(默认父项为空项)）
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):

        parentItem = self.getItem(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        isSuccess = False
        for i in range(rows):
            isSuccess = parentItem.removeChild(position)

        self.endRemoveRows()

        return isSuccess


class TreeModel_Proj_Task(TreeModel):
    def __init__(self, item, parent=None):
        super(TreeModel_Proj_Task, self).__init__(parent)

        # 设置初始项的item
        self._rootItem = item
        self.updateChild()

    # 插入单行数据
    def insertRow(self, position, parent=QtCore.QModelIndex(), data=None):
        parentItem = self.getItem(parent)
        parentID = parentItem._dbId
        if data == None:
            data = configure.get_DB_Struct('empty_taskInfo') # 从配置文件获取插入的空内容(list)
            data[0] = parentID
        # print(data)
        # 数据库插入项并获取其id
        dbid = DB.insertData(configure.getProjectPath(), 'table_taskInfo', configure.struct_taskInfo, data)
        
        # 获取并更新父级 childrenID 数据
        childrenID = self.getChildrenIdList(parent)
        if parent != QtCore.QModelIndex():
            childrenID.insert(position, dbid) # 插入id到childrenID
            childrenIdStr = str(childrenID)[1:-1] # list转为文字并去掉首尾字符（[])
            # 更新父级item 数据
            parentItem._itemData[3] = childrenIdStr
            # 更新父级数据库数据
            DB.updateData(configure.getProjectPath(), 'table_taskInfo',  'id=%d' %(parentID), 'childrenID="%s"'%childrenIdStr)

        data.insert(0, dbid) # 将ID添加到插入数据中
        # print(data)
        item = BaseTreeItem(data)
        self.insertRows(position, 1, parent, [item])

    # 删除单行数据（插入位置， 父项(默认父项为空项)）
    def removeRow(self, position, parent=QtCore.QModelIndex()):

        parentItem = self.getItem(parent)
        parentID = parentItem._dbId
        dbid = parentItem.child(position)._dbId # 获取要删除项的ID

        # 获取并更新父级 childrenID 数据
        childrenID = self.getChildrenIdList(parent)
        if parent != QtCore.QModelIndex():
            childrenID.remove(dbid) # 删除id 从childrenID
            childrenIdStr = str(childrenID)[1:-1] # list转为文字并去掉首尾字符（[])
            # 更新父级item 数据
            parentItem._itemData[3] = childrenIdStr
            # 更新父级数据库数据
            DB.updateData(configure.getProjectPath(), 'table_taskInfo',  'id=%d' %(parentID), 'childrenID="%s"'%childrenIdStr)

        # 从数据库删除项
        DB.deleteData(configure.getProjectPath(), 'table_taskInfo', 'id=%d' %(dbid))
        # 从树删除
        self.removeRows(position, 1, parent)
        
    # 更新子项
    def updateChild(self, parent=QtCore.QModelIndex()):
        # 删除现有子项
        if self.rowCount(parent) > 0:
            self.removeRows(0, self.rowCount(parent), parent)

        items = []
        parentItem = self.getItem(parent)
        # 添加子项(父项为root项时)
        if parent==QtCore.QModelIndex():
            dbdatas = DB.findDatas(configure.getProjectPath(), 'table_taskInfo', 'parentID=-1')
            for itemdata in dbdatas:
                # print(itemdata)
                items.append(BaseTreeItem(itemdata, parentItem))# 添加行

        childrenID = self.getChildrenIdList(parent)
        # 添加子项(父项非root项时)
        if childrenID != None:
            for i in childrenID:
                # if str.isdigit(i):  # 判断是否为正整数
                dbdatas = DB.findData(configure.getProjectPath(), 'table_taskInfo', 'id=%s'%i)
                itemdata = dbdatas
                items.append(BaseTreeItem(itemdata, parentItem)) # 根据childrenID添加行
        
        # 添加二级子项
        for item in items:
            itemIndex =  self.index(item.row(), 0, parent)
            self.updateChild(itemIndex)


    # 获取 childrenID ，并转化为数字列表
    def getChildrenIdList(self, parent=QtCore.QModelIndex()):
        if parent == QtCore.QModelIndex():
            return None
        parentItem = self.getItem(parent)
        # 获取数据
        datas = parentItem.datas()
        # 获取子项
        if datas[3] != '':
            childrenIdStr = datas[3].split(',') # 分割childrenID，转化为列表
            childrenID = []
            # 将文字列表转为数字列表
            for i in childrenIdStr:
                childrenID.append(int(i))
            return childrenID
        return []



# ----------------------------- Item class 部件 -------------------------------- #
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
        # 多个添加条目
        editor.addItems(['功能', '错误', '改进', '重构', '研究', '测试', '文件'])
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
        # 当下拉索引发生改变时发射信号触发绑定的事件
        editor.currentIndexChanged.connect(
            lambda: self.selectionchange(editor))

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
            now = QtCore.QDate.currentDate()  # 获取当前日期
            editor.setDate(now)

    # 从编辑器窗口小部件获取数据，并将其存储在项索引处的指定模型中。
    def setModelData(self, editor, model, index):
        # current_Date = time.strftime("%Y-%m-%d", editor.date())
        current_Date = editor.date()
        print(current_Date.toString(QtCore.Qt.ISODate))  # ISO日期格式打印
        # print(current_Date.toString(Qt.DefaultLocaleLongDate)) #本地化长格式日期打印(2018年1月14日 )
        value = current_Date.toString(QtCore.Qt.ISODate)

        model.setData(index, value, QtCore.Qt.EditRole)

    # 根据给定的样式选项更新索引指定的项目的编辑器。
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

# 数字显示框


class SpinBoxDelegate(QtWidgets.QItemDelegate):
    '''
    '''
    # createEditor 返回用于更改模型数据的小部件，可以重新实现以自定义编辑行为。

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QSpinBox(parent)
        editor.setFrame(False)
        editor.setFrame(False)
        editor.setMinimum(0)
        editor.setMaximum(100)

        return editor

    # 设置编辑器从模型索引指定的数据模型项中显示和编辑的数据。
    def setEditorData(self, spinBox, index):
        value = index.model().data(index, QtCore.Qt.EditRole)

        spinBox.setValue(6)

    # 从编辑器窗口小部件获取数据，并将其存储在项索引处的指定模型中。
    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()

        model.setData(index, value, QtCore.Qt.EditRole)

    # 根据给定的样式选项更新索引指定的项目的编辑器。
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
