#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# amConfigure.py
# @Author : Ivan-杨杨兮 (523166477@qq.com)
# @Link   : www.cgartech.com
# @Date   : 2019/3/4 下午11:05:47


import os
import json


# ------------------------------ 本地配置文件 ------------------------------- #
# 获取配置文件
localConfigPath = os.path.dirname(os.path.dirname(__file__)) + '/config/LocalConfigure.json'

localConfigStruct = {
    'lastProject' : 'DefaultProject',
    'DefaultProject' : {
        'projectPath' : '',
        'collectionPath' : []
    }  
}

# 读取配置文件信息
def loadConfig():
    if os.path.exists(localConfigPath): # 判断文件是否存在
        f = open(localConfigPath, 'r')
        try:
            data = json.loads(f.read())
            f.close()
            return data
        except Exception as e:
            f.close()
            print('LocalConfigure loadConfig error:%s'%(e))

# 获得所有工程名称
def getAllProjectNames():
    try:
        data = loadConfig()
        AllProjectName = list(data.keys()) # 返回一个字典所有的键, 转换为列表形式
        if ('lastProject' in AllProjectName) and len(AllProjectName) > 1: # 判断字典是否存在某个key
            AllProjectName.remove('lastProject')
            return AllProjectName
    except Exception as e:
        f = open(localConfigPath, 'w')
        f.write(json.dumps(localConfigStruct)) 
        f.close()
        print('LocalConfigure getAllProjectNames error:%s'%(e))
        return ['DefaultProject']

# 获取最后一次打开的工程名称
def getLastProjectName():
    try:
        data = loadConfig()
        if ('lastProject' in data.keys()): # 判断字典是否存在某个key
            if (data['lastProject'] in data.keys()):
                # 判断最后一次打开的工程路径是否存在
                if os.path.exists(data[data['lastProject']]['projectPath']):
                    return data['lastProject']
                else:
                    data['lastProject'] = 'DefaultProject'
                    f = open(localConfigPath, 'w')
                    f.write(json.dumps(data)) 
                    f.close()
                    return 'DefaultProject'
            else:
                f = open(localConfigPath, 'w')
                f.write(json.dumps(data)) 
                f.close()
                return 'DefaultProject'
        else:
            f = open(localConfigPath, 'w')
            f.write(json.dumps(localConfigStruct)) 
            f.close()
            return 'DefaultProject'
    except Exception as e:
        f = open(localConfigPath, 'w')
        f.write(json.dumps(localConfigStruct)) 
        f.close()
        print('LocalConfigure getLastProjectName error:%s'%(e))
        return 'DefaultProject'

# 设置最后一次打开的工程名称
def setLastProjectName(name):
    data = loadConfig()
    data['lastProject'] = name
    f = open(localConfigPath, 'w')
    f.write(json.dumps(data)) 
    f.close()

# 添加新工程
def addNewProject(name, path):
    data = loadConfig()
    if not (name in data.keys()):
        data[name] = {
            'projectPath' : path,
            'collectionPath' : []
        }
        data['lastProject'] = name
        f = open(localConfigPath, 'w')
        f.write(json.dumps(data)) 
        f.close()
        return True
    else:
        return False

# 移除工程
def removeProject(name):
    data = loadConfig()
    if (name in data.keys()):
        del data[name]

# ------------ 工程目录 --------------------- #
def getProjectPath():
    try:
        data = loadConfig()
        if os.path.isdir(data[getLastProjectName()]['projectPath']):
            return data[getLastProjectName()]['projectPath']
        else:
            return ''
    except Exception as e:
        print('LocalConfigure getProjectPath error:%s'%e)

def setProjectPath(path):
    if not os.path.exists(path):
        os.makedirs(path) # 创建路径
    try:
        data = loadConfig()
        data[getLastProjectName()]['projectPath'] = os.path.abspath(path)
        f = open(localConfigPath, 'w')
        f.write(json.dumps(data)) 
        f.close()
    except Exception as e:
        print('LocalConfigure setProjectPath error:%s'%e)

# ------------ 分支 ---------------- #
# def getProjectBranch():
#     try:
#         data = loadConfig()
#         return data[getLastProjectName()]['branch']
#     except Exception as e:
#         data = loadConfig()
#         data[getLastProjectName()]['branch'] = ''
#         f = open(localConfigPath, 'w')
#         f.write(json.dumps(data)) 
#         f.close()
#         print('LocalConfigure error:%s'%e)
#         return ''

# def setProjectBranch(branch):
#     try:
#         data = loadConfig()
#         data[getLastProjectName()]['branch'] = branch
#         f = open(localConfigPath, 'w')
#         f.write(json.dumps(data)) 
#         f.close()
#     except Exception as e:
#         print('LocalConfigure error:%s'%e)

# ------------ 收藏目录 --------------------- #
def getCollectionPath():
    if os.path.exists(localConfigPath): # 判断文件是否存在
        try:
            data = loadConfig()
            return data[getLastProjectName()]['collectionPath']
        except Exception as e:
            print('LocalConfigure error:%s'%e)

def addCollectionPath(path):
    if os.path.exists(path):
        data = loadConfig()
        if not path in data[getLastProjectName()]['collectionPath']:
            data[getLastProjectName()]['collectionPath'].append(path)
            f = open(localConfigPath, 'w')
            f.write(json.dumps(data)) 
            f.close()

def removeCollectionPath(path):
    data = loadConfig()
    if path in data[getLastProjectName()]['collectionPath']:
        data[getLastProjectName()]['collectionPath'].remove(path)
        f = open(localConfigPath, 'w')
        f.write(json.dumps(data)) 
        f.close()




# ------------------------------ 项目配置文件 ------------------------------- #
def setProjectConfig():
    path = getProjectPath() + '/config/projectConfig.ini'
    # if not os.path.exists(path):
    #     os.makedirs(path) # 创建路径
    try:
        # data = loadConfig()
        # data[getLastProjectName()]['projectPath'] = os.path.abspath(path)
        f = open(path, 'w')
        f.write(json.dumps(data)) 
        f.close()
    except Exception as e:
        print('LocalConfigure setProjectPath error:%s'%e)



if __name__ == '__main__':
    print(getProjectPath())
    setProjectPath("./data/TestData")