#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# AM_db.py
# @Author : Ivan-杨杨兮 (523166477@qq.com)
# @Link   : www.cgartech.com
# @Date   : 2019/3/2 上午10:27:25


import sqlite3
import os
import re
import configure

# 用于创建列表
 # 建立自增主键:id integer primary key autoincrement
create_taskInfo = '(id integer primary key autoincrement,' + configure.get_DB_Struct_ToString('create_taskInfo') + ')'

# 用于初始化列表
struct_taskInfo = configure.get_DB_Struct_ToString('struct_taskInfo')


# 数据库路径
def dbPath():
    projectPath = configure.getProjectPath()
    if os.path.isdir(projectPath):
        Path = projectPath + '/data/db.db'
        # 检查文件夹是否存在，不存在则创建
        if not os.path.exists(projectPath + '/data'): # 判断是否是目录
            os.makedirs(projectPath + '/data') # 创建路径
        return Path
    else:
        return ''


# 执行操作
def executeDB(query):
    conn = sqlite3.connect(dbPath()) # 连接数据库
    conn.text_factory = str
    cursor = conn.cursor()

    result = cursor.execute(query) # 执行操作
    students = result.fetchall()

    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接
    return students

# 执行多次操作
def executemanyDB(query, data):
    conn = sqlite3.connect(dbPath()) # 连接数据库
    conn.text_factory = str
    cursor = conn.cursor()

    result = cursor.executemany(query, data) # 执行多次操作
    students = result.fetchall()

    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接
    return students


# 创建sqlite3数据表
def CreateTable(tableName, createTableStruct):
    conn = sqlite3.connect(dbPath()) # 连接数据库
    conn.text_factory = str
    
    # 执行操作:创建表
    conn.execute("create table IF NOT EXISTS " + tableName + " " +createTableStruct)

    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接

# 重新创建数据表
def reCreateTable(tableName, createTableStruct):
    conn = sqlite3.connect(dbPath()) # 连接数据库
    conn.text_factory = str
    
    conn.execute("drop table IF EXISTS %s"%(tableName)) # 删除表

    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接

    CreateTable(tableName, createTableStruct) # 创建表

# 插入行
def insertData(tableName, tableStruct, data):
    conn = sqlite3.connect(dbPath()) # 连接数据库
    conn.text_factory = str
    try:
        conn.execute("insert into " + tableName + "(" + tableStruct + \
            ")" + "VALUES (?%s)"%(',?'*(len(re.findall(r',', tableStruct)))), data) # 执行操作
    except Exception as e:
        print(e)
    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接

# 插入多行
def insertManyData(tableName, tableStruct, datas):
    conn = sqlite3.connect(dbPath()) # 连接数据库
    conn.text_factory = str
    try:
        conn.executemany("insert into " + tableName + "(" + tableStruct + \
            ")" + "VALUES (?%s)"%(',?'*(len(re.findall(r',', tableStruct)))), datas) # 执行操作
    except Exception as e:
        print(e)
    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接

# 插入列
def insertColumn(tableName, columnName, columnType):
    conn = sqlite3.connect(dbPath()) # 连接数据库
    conn.text_factory = str
    try:
        # ALTER  TABLE   table-name  ADD COLUMN  column-name column-type
        conn.execute("alter table " + tableName + " add column " + columnName + " " + columnType) # 执行操作
    except Exception as e:
        print(e)
    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接

# 查询数据
def findData(tableName, theData, keys=''):
    conn = sqlite3.connect(dbPath()) # 连接数据库
    cursor = conn.cursor()

    if keys == '':
        result = cursor.execute('SELECT * FROM ' + tableName + ' WHERE ' + theData) # 执行操作
    else:
        result = cursor.execute('SELECT ' + keys + ' FROM ' + tableName + ' WHERE ' + theData) # 执行操作
    student = result.fetchone()

    # conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接
    return student
    
# 查询数据（返回列表）
def findDatas(tableName, theData, keys=''):
    conn = sqlite3.connect(dbPath()) # 连接数据库
    cursor = conn.cursor()

    if keys == '':
        result = cursor.execute('SELECT * FROM ' + tableName + ' WHERE ' + theData) # 执行操作
    else:
        result = cursor.execute('SELECT ' + keys + ' FROM ' + tableName + ' WHERE ' + theData) # 执行操作
    students = result.fetchall()

    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接
    return students

# 遍历数据（返回列表）
def getDatas(tableName, keys=''):
    conn = sqlite3.connect(dbPath()) # 连接数据库
    cursor = conn.cursor()

    if keys == '':
        result = cursor.execute('SELECT * FROM ' + tableName) # 执行操作
    else:
        result = cursor.execute('SELECT ' + keys + ' FROM ' + tableName) # 执行操作
    students = result.fetchall()

    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接
    return students

# 删除数据
def deleteData(tableName, theData):
    conn = sqlite3.connect(dbPath()) # 连接数据库
    try:
        conn.execute('DELETE FROM ' + tableName + ' WHERE ' + theData) # 执行操作
    except Exception as e:
        print(e)
    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接

# 修改数据
def updateData(tableName, theData, newData):
    conn = sqlite3.connect(dbPath()) # 连接数据库
    try:
        conn.execute('UPDATE ' + tableName + ' SET ' + newData + ' WHERE ' + theData) # 执行操作
    except Exception as e:
        print(e)
    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接

# 重建所有表
def reCreateAll():
    # CreateTable(tableName, createTableStruct)
    reCreateTable('table_taskInfo', create_taskInfo)
    # # 初始化状态列表
    # insertManyData('state', struct_taskInfo, (
    #     ('完成', '#61bd4f'), 
    #     ('', '#f2d600'), 
    #     ('', '#ff9f1a'),
    #     ('', '#eb5a46'), 
    #     ('', '#c377e0'),
    #     ('', '#f2d600'),
    #     ('进行中', '#0079bf'), 
    #     ('', '#355263')
    #     ))

if __name__ == '__main__':
    print(dbPath())
    # CreateTable('table_taskInfo', create_taskInfo)
    reCreateTable('table_taskInfo', create_taskInfo)
    # insertColumn('table_taskInfo', 'adds', 'int')
    # insertData('list', struct_taskInfo, ('nnn', False, 'aaa', 'bbb'))
    # updateData('list', 'listName="n11"', 'listName="g11",listComplete=1')
    # deleteData('list', 'listName="n22"')
    # print(findData('list', "listName='g11'")[0])
    # print(findData('list', "listName='g11'", 'listName'))
    # print(findData('list', "listName='g11'"))