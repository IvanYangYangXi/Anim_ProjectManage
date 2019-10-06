#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# treeModels.py
# @Author :  ()
# @Link   :
# @Date   : 7/10/2019, 2:58:31 PM


import sys, os
import shutil
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
            return item.data(index.column())
                

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
                # print(item.datas)
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
            # print(childItem.datas())

        self.endInsertRows()
        
        return isSuccess

    # 删除多行数据（插入位置， 插入行数， 父项(默认父项为空项)）
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        if not parent.isValid():
            return False
        if rows <= 0:
            return False
        parentItem = self.getItem(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        isSuccess = False
        for i in range(rows):
            isSuccess = parentItem.removeChild(position)

        self.endRemoveRows()

        return isSuccess

    # 获取当前项的首列 index
    def getColumnIndex(self, index, column=0):
        currentItem = self.getItem(index)
        currentIndex = self.index(currentItem.row(), column, index.parent())
        return currentIndex


class TreeModel_Proj_Task(TreeModel):
    def __init__(self, item, parent=None):
        super(TreeModel_Proj_Task, self).__init__(parent)

        # 设置初始项的item
        self._rootItem = item
        # 数据更新时调用的函数
        self.func = None

        self.updateChild()
    
        # 返回索引项目存储的数据。
    def data(self, index, role):
        if not index.isValid():
            return None

        # item = index.internalPointer()
        item = self.getItem(index)
        imgPath = item.data(1) # 获取缩略图路径

        # 设置行高
        if role == QtCore.Qt.SizeHintRole:
            # 返回单元格尺寸
            return QtCore.QSize(0, 40)

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 1: # 缩略图列
                return ''
            else:
                return item.data(index.column())

        # 设置图标 state
        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0: # 设置图标
                # print(item.data(2))
                # print("任务")
                if item.data(2).encode("utf-8") == "任务":
                    return QtGui.QIcon(QtGui.QPixmap('./UI/point_blue.png'))
                elif item.data(2).encode("utf-8") == "用户故事":
                    return QtGui.QIcon(QtGui.QPixmap('./UI/point_green.png'))
                else:
                    return QtGui.QIcon(QtGui.QPixmap('./UI/point_gray.png')) 
            if index.column() == 1: # 缩略图列
                if os.path.isfile(imgPath): # 判断文件
                    if imgPath.endswith(('.jpg', '.jpge', '.png', '.tga', '.gif')):
                        return QtGui.QIcon(QtGui.QPixmap(imgPath))
                return QtGui.QIcon(QtGui.QPixmap('./UI/img_loss.jpg'))
                
    # 编辑数据
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            item = index.internalPointer()

            if role == QtCore.Qt.EditRole:
                # if index.column() == 1:
                item.setData(value, index.column())
                self.dataChanged.emit(index, index)  # 更新Model的数据

                # 数据更新时调用的函数
                if self.func != None:
                    self.func()
                return True
        return False

    # 通过详细面板更新数据，不执行函数调用
    def setDataByDetail(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            item = index.internalPointer()

            if role == QtCore.Qt.EditRole:
                # if index.column() == 1:
                item.setData(value, index.column())
                # print(item.datas)
                self.dataChanged.emit(index, index)  # 更新Model的数据
                return True
        return False

    # 通过详细面板更新item 所有数据，不执行函数调用
    def setAllDatasByDetail(self, index, datas, role=QtCore.Qt.EditRole):
        if index.isValid():
            item = index.internalPointer()

            if role == QtCore.Qt.EditRole:
                # if index.column() == 1:
                # item._itemData = datas
                datas = datas[8:]
                # 更新数据库数据
                x = 3
                for i in datas:
                    x += 1
                    item.setData(i, x)
                    index_X = self.index(index.row(), x, index.parent())
                    self.dataChanged.emit(index_X, index_X)  # 更新Model的数据
                return True
        return False

    # 返回一组标志
    def flags(self, index):

        # 复选框
        # if index.column() == 1:
        #     return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable

        # 基类实现返回一组标志，标志启用item（ItemIsEnabled），并允许它被选中（ItemIsSelectable）。
        if index.column() == 1:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    # 插入单行数据
    def insertRow(self, position, parent=QtCore.QModelIndex(), data=None):
        parentItem = self.getItem(parent)
        parentID = parentItem._dbId
        if data == None:
            data = configure.get_DB_Struct('empty_taskInfo') # 从配置文件获取插入的空内容(list)
            data[0] = parentID
        # print(data)
        # 数据库插入项并获取其id
        dbid = DB.insertData(configure.getProjectPath(), 'table_taskInfo', configure.struct_taskInfo(), data)
        
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

        filePath = configure.getProjectPath() + '/data/Content/%s'%dbid
        if not os.path.exists(filePath):
            os.makedirs(filePath) # 创建路径

        return self.index(position, 0, parent) # 返回插入项的index

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

        filePath = configure.getProjectPath() + '/data/%s'%dbid
        shutil.rmtree(filePath, True)    #递归删除文件夹,True参数表示ignore_errors(忽略错误)。
        
    # 更新子项
    def updateChild(self, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)
        # 删除现有子项
        if self.rowCount(parent) > 0:
            self.removeRows(0, self.rowCount(parent), parent)
        items = []
        # 添加子项(父项为root项时)
        if parent==QtCore.QModelIndex():
            dbdatas = DB.findDatas(configure.getProjectPath(), 'table_taskInfo', 'parentID=-1')
            for itemdata in dbdatas:
                # print(itemdata)
                items.append(BaseTreeItem(itemdata, parentItem))# 添加行
        childrenID = self.getChildrenIdList(parent) # 获取 childrenID 列表
        # 添加子项(父项非root项时)
        if childrenID != None:
            for ci in childrenID:
                # if str.isdigit(i):  # 判断是否为正整数
                dbdatas = DB.findData(configure.getProjectPath(), 'table_taskInfo', 'id=%s'%ci)
                itemdata = dbdatas
                items.append(BaseTreeItem(itemdata, parentItem)) # 根据childrenID添加行
        # 添加二级子项
        for item in items:
            itemIndex =  self.index(item.row(), 0, parent)
            # self.updateChild(itemIndex)

            # 获取 childrenID 列表
            secChildrenID = self.getChildrenIdList(itemIndex)
            if secChildrenID != None:
                for sci in secChildrenID:
                    # if str.isdigit(i):  # 判断是否为正整数
                    dbdatas = DB.findData(configure.getProjectPath(), 'table_taskInfo', 'id=%s'%sci)
                    itemdata = dbdatas
                    BaseTreeItem(itemdata, item) # 根据childrenID添加行

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
class ComboBoxDelegate(QtWidgets.QItemDelegate):
    '''
    在应用它的列的每个单元格中放置一个功能齐全的QComboBox的委托
    '''
    def __init__(self, combos, defaultComboId=0):
        QtWidgets.QItemDelegate.__init__(self)
        self.combos = configure.get_DB_Struct(combos)
        self.defaultComboId = int(defaultComboId)
        self.func = None

    # createEditor 返回用于更改模型数据的小部件，可以重新实现以自定义编辑行为。
    def createEditor(self, parent, option, index):

        # taskType = configure.get_DB_Struct('TaskType')

        editor = QtWidgets.QComboBox(parent)
        # editor.addItem('项目')
        # 多个添加条目
        editor.addItems(self.combos)
        # 当下拉索引发生改变时发射信号触发绑定的事件
        # editor.currentIndexChanged.connect(
        #     lambda: self.currentIndexDataChanged(editor))

        return editor

    def currentIndexDataChanged(self, editor):
        # currentText()：返回选中选项的文本
        # ct = editor.currentText()
        # print('Items in the list are:' + ct)
        if self.func != None:
            self.func()

    # 设置编辑器从模型索引指定的数据模型项中显示和编辑的数据。
    def setEditorData(self, editor, index):
        data = index.model().data(index, QtCore.Qt.EditRole)
        # taskType = configure.get_DB_Struct('TaskType')

        if data in self.combos:
            self.defaultComboId = self.combos.index(data)

        # 避免不是由用户引起的信号,因此我们使用blockSignals.
        editor.blockSignals(True)
        # ComboBox当前项使用setCurrentIndex()来设置
        editor.setCurrentIndex(self.defaultComboId)
        editor.blockSignals(False)

    # 从编辑器窗口小部件获取数据，并将其存储在项索引处的指定模型中。
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)

    # 根据给定的样式选项更新索引指定的项目的编辑器。
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)



# 时间选择控件
class DateEditDelegate(QtWidgets.QItemDelegate):
    '''
    在应用它的列的每个单元格中放置一个功能齐全的QComboBox的委托
    '''
    def __init__(self):
        QtWidgets.QItemDelegate.__init__(self)
        self.func = None

    # self.dateEdit = QtGui.QDateEdit(QtCore.QDate.currentDate())
    # self.dateEdit.setDisplayFormat('yyyy-MM-dd')
    # self.dateEdit.setCalendarPopup(True)
    # createEditor 返回用于更改模型数据的小部件，可以重新实现以自定义编辑行为。
    def createEditor(self, parent, option, index):
        editor = QtWidgets.QDateEdit(parent)
        editor.setDisplayFormat('yyyy-MM-dd')
        editor.setCalendarPopup(True)
        # editor.timeChanged.connect(
        #     lambda: self.currentIndexDataChanged(editor))

        return editor

    def currentIndexDataChanged(self, editor):
        if self.func != None:
            self.func()

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


# 整数数字显示框
class SpinBoxDelegate(QtWidgets.QItemDelegate):
    '''
    '''
    def __init__(self):
        QtWidgets.QItemDelegate.__init__(self)
        self.func = None

    # createEditor 返回用于更改模型数据的小部件，可以重新实现以自定义编辑行为。

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QSpinBox(parent)
        editor.setFrame(False)
        editor.setFrame(False)
        editor.setMinimum(0)
        editor.setMaximum(1000)
        # editor.valueChanged.connect(
        #     lambda: self.currentIndexDataChanged(editor))

        return editor

    def currentIndexDataChanged(self, editor):
        if self.func != None:
            self.func()

    # 设置编辑器从模型索引指定的数据模型项中显示和编辑的数据。
    def setEditorData(self, spinBox, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        # print(int(value))
        if value != '':
            try:
                spinBox.setValue(int(value))
            except Exception as e:
                spinBox.setValue(0)
                print('SpinBoxDelegate error:%s' % (e))
        else:
            spinBox.setValue(0)

    # 从编辑器窗口小部件获取数据，并将其存储在项索引处的指定模型中。
    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()

        model.setData(index, value, QtCore.Qt.EditRole)

    # 根据给定的样式选项更新索引指定的项目的编辑器。
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


# 小数数字显示框
class DoubleSpinBoxDelegate(QtWidgets.QItemDelegate):
    '''
    '''
    def __init__(self):
        QtWidgets.QItemDelegate.__init__(self)
        self.func = None

    # createEditor 返回用于更改模型数据的小部件，可以重新实现以自定义编辑行为。

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setFrame(False)
        editor.setFrame(False)
        editor.setMinimum(0)
        editor.setMaximum(1000)
        # editor.valueChanged.connect(
        #     lambda: self.currentIndexDataChanged(editor))

        return editor

    def currentIndexDataChanged(self, editor):
        if self.func != None:
            self.func()

    # 设置编辑器从模型索引指定的数据模型项中显示和编辑的数据。
    def setEditorData(self, spinBox, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        # print(int(value))
        if value != '':
            try:
                spinBox.setValue(float(value))
            except Exception as e:
                spinBox.setValue(0)
                print('DoubleSpinBoxDelegate error:%s' % (e))
        else:
            spinBox.setValue(0)

    # 从编辑器窗口小部件获取数据，并将其存储在项索引处的指定模型中。
    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()

        model.setData(index, value, QtCore.Qt.EditRole)

    # 根据给定的样式选项更新索引指定的项目的编辑器。
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
