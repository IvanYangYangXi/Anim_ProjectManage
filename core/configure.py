#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# amConfigure.py
# @Author : Ivan-杨杨兮 (523166477@qq.com)
# @Link   : www.cgartech.com
# @Date   : 2019/3/4 下午11:05:47


import os
import json
import DB


# ------------------------------ 本地配置文件 ------------------------------- #
# 获取配置文件
localConfigPath = os.path.dirname(os.path.dirname(
    __file__)) + '/config/LocalConfigure.json'

localConfigStruct = {
    'lastProject': 'DefaultProject',
    'DefaultProject': {
        'projectPath': '',
        'collectionPath': []
    }
}


# 读取配置文件信息
def loadConfig():
    if os.path.exists(localConfigPath):  # 判断文件是否存在
        f = open(localConfigPath, 'r')
        try:
            data = json.loads(f.read())
            f.close()
            return data
        except Exception as e:
            f.close()
            print('LocalConfigure loadConfig error:%s' % (e))


# 获得所有工程名称
def getAllProjectNames():
    try:
        data = loadConfig()
        AllProjectName = list(data.keys())  # 返回一个字典所有的键, 转换为列表形式
        if ('lastProject' in AllProjectName) and len(AllProjectName) > 1:  # 判断字典是否存在某个key
            AllProjectName.remove('lastProject')
            return AllProjectName
    except Exception as e:
        f = open(localConfigPath, 'w')
        f.write(json.dumps(localConfigStruct))
        f.close()
        print('LocalConfigure getAllProjectNames error:%s' % (e))
        return ['DefaultProject']


# 获取最后一次打开的工程名称
def getLastProjectName():
    try:
        data = loadConfig()
        if ('lastProject' in data.keys()):  # 判断字典是否存在某个key
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
        print('LocalConfigure getLastProjectName error:%s' % (e))
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
            'projectPath': path,
            'collectionPath': []
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
        print('LocalConfigure getProjectPath error:%s' % e)
        return ''


def setProjectPath(path):
    if not os.path.exists(path):
        os.makedirs(path)  # 创建路径
    try:
        data = loadConfig()
        data[getLastProjectName()]['projectPath'] = os.path.abspath(path)
        f = open(localConfigPath, 'w')
        f.write(json.dumps(data))
        f.close()
    except Exception as e:
        print('LocalConfigure setProjectPath error:%s' % e)


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
    if os.path.exists(localConfigPath):  # 判断文件是否存在
        try:
            data = loadConfig()
            return data[getLastProjectName()]['collectionPath']
        except Exception as e:
            print('LocalConfigure error:%s' % e)


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
'''
    注：数据库使用自增id， [0-3]在treeItem中不显示（id，父级，排序，子级），
            [4-7]在详细信息固定栏显示（'任务','缩略图','类型','状态',）
    create_taskInfo: DB 创建数据库的Key 及 type （不含id）
    struct_taskInfo: DB 数据对应的key （不含id）
    rootNode_taskInfo: 标题行标签内容
    empty_taskInfo: 空数据时的默认数据，DB Item 的默认数据
    dataTypes: 自定义数据类型：
                    整数：'int'
                    小数：'float'
                    单行文本：'text'
                    多行文本：'longText'
                    英文字符: 'string'
                    人员：'personnel'
                    时间：'date'
                    下拉选择框：'combo:下拉框关键字:默认项id'【'combo:TaskType:5'】
    
    下拉框关键字对应选项
        TaskType: 对应任务类型
        TaskState: 对应任务状态
        priority: 对应任务优先级
'''
db_Struct = {
    'create_taskInfo': [
        'parentID int',
        'sort text',
        'childrenID text',
        'task NVARCHAR(100)',
        'img text',
        'type NCHAR(30)',
        'state NCHAR(20)',
        'abbreviation CHAR(50)',
        'label NCHAR(50)'
        'executive NCHAR(20)',
        'reporter NCHAR(20)',
        'priority NCHAR(20)',
        'description text',
        'deadline CHAR(20)',
        'estimateTime CHAR(20)',
        'remaining CHAR(20)'
    ],
    'struct_taskInfo': [
        'parentID',
        'sort',
        'childrenID',
        'task',
        'img',
        'type',
        'state',
        'abbreviation',
        'label'
        'executive',
        'reporter',
        'priority',
        'description',
        'deadline',
        'estimateTime',
        'remaining'
    ],
    'rootNode_taskInfo': [
        -1,
        -2,
        '0',
        '',
        '任务',
        '缩略图',
        '类型',
        '状态',
        '英文简称',
        '标签',
        '执行人',
        '报告人',
        '优先级',
        '描述',
        '截止日期',
        '预估时间（小时）',
        '结余（小时）'
    ],
    'empty_taskInfo': [
        -1,
        '0',
        '',
        'taskName',
        '',
        '任务',
        '待办',
        '',
        '',
        'executive',
        'reporter',
        'medium',
        '描述',
        '',
        '',
        ''
    ],
    'dataTypes': [
        'int',
        'int',
        'text',
        'text',
        'text',
        'img',
        'combo:TaskType:5',
        'combo:TaskState:0',
        'string',
        'text',
        'personnel',
        'personnel',
        'combo:priority:1',
        'longText',
        'date',
        'float',
        'float'
        ],
    'fileInfoBy':{
        'prefix':{
            'default': '',
            '模型,贴图':'SM_',
            '绑定,融合变形':'SK_'
        },
        'suffix':{
            'default': ''
        },
        'fileType':{
            'source':['.mb', '.ma', '.max', '.ZBR', '.zbr', '.ZTL', '.ztl'],
            'mesh':['.fbx', '.abc', '.FBX', '.ABC', '.obj', '.OBJ'],
            'texture':['.tga', '.TGA', '.jpg', '.jpeg', '.png', '.dds']
        },
        'pathBy':{
            'default': '/Content/SourceFile',
            'source':'/Content/SourceFile',
            'mesh':'/Content/Meshes',
            'texture':'/Content/Textures'
        }
    },
    'label':['剧集', '场次', '镜头', '资产', '角色', '场景', '模型', '贴图', '材质', '绑定', '融合变形', '动画', '灯光', '地编', '特效', '开发'],
    'TaskType': ['项目', '史诗故事', '主题故事', '用户故事', '任务', '里程碑', '信息', '文件夹', '功能', '错误', '改进', '重构', '研究', '测试', '文件'],
    'TaskState': ['待办', '进行中', '提交审核', '审核通过', '返修'],
    'priority': ['hight', 'medium', 'low']
}

# projectConfigPath() = getProjectPath() + '/config/projectConfig.ini'


# 读取项目配置文件信息
def loadProjectConfig():
    if not os.path.exists(getProjectPath() + '/config/projectConfig.ini'):  # 判断文件是否存在
        createProjectConfig()
    # 读取文件信息
    f = open(getProjectPath() + '/config/projectConfig.ini', 'r')
    try:
        data = json.loads(f.read())
        f.close()
        return data
    except Exception as e:
        f.close()
        print('ProjectConfigure loadProjectConfig error:%s' % (e))


# 更新项目配置文件信息
def updateProjectConfig(data):
    if not os.path.exists(getProjectPath() + '/config/projectConfig.ini'):  # 判断文件是否存在
        createProjectConfig()
    try:
        f = open(getProjectPath() + '/config/projectConfig.ini', 'w')
        f.write(json.dumps(data))
        f.close()
    except Exception as e:
        print('ProjectConfigure updateProjectConfig error:%s' % e)


# 创建项目配置文件及数据表
def createProjectConfig():
    if not os.path.exists(getProjectPath() + '/config'):
        os.makedirs(getProjectPath() + '/config')  # 创建路径
    if not os.path.exists(getProjectPath() + '/config/projectConfig.ini'):  # 判断文件是否存在
        # 创建配置文件
        # print(getProjectPath())
        f = open(getProjectPath() + '/config/projectConfig.ini', 'w')
        f.write(json.dumps(db_Struct))
        f.close()
    if not os.path.exists(getProjectPath() + '/data/db.db'):  # 判断文件是否存在
        # 创建表
        DB.CreateTable(getProjectPath(), 'table_taskInfo', create_taskInfo())
        print('ProjectConfigure createProjectConfig : Create New Project Config')


def get_DB_Struct(variable):
    try:
        data = loadProjectConfig()
        if not data.has_key(variable):  # 如果Key不存在
            if db_Struct.has_key(variable):
                data[variable] = db_Struct[variable]  # 添加
                updateProjectConfig(data)  # 更新项目配置文件
        struct = data[variable]
        # print(struct)
        return struct
    except Exception as e:
        print('ProjectConfigure get_DB_Struct error:%s' % e)


def get_DB_Struct_ToString(variable):
    try:
        data = loadProjectConfig()
        if not data.has_key(variable):  # 如果Key不存在
            if db_Struct.has_key(variable):
                data[variable] = db_Struct[variable]  # 添加
                updateProjectConfig(data)  # 更新项目配置文件
        # print(data[variable])
        struct = ''
        for i in data[variable]:
            if type(i)==int:
                i = str(i).encode("utf-8")
            struct = struct + i + ', '
        struct = struct[:-2]  # 去掉最后一个(多个)字符
        # print(struct)
        return struct
    except Exception as e:
        print('ProjectConfigure get_DB_Struct_ToString error:%s' % e)


# 根据标签获取id
def getIndexByLabel(label):
    labels = get_DB_Struct('rootNode_taskInfo')
    if label in labels:
        return labels.index(label)
    else:
        return None


# 用于创建列表
# 建立自增主键:id integer primary key autoincrement
def create_taskInfo():
    create_taskInfo = '(id integer primary key autoincrement,' + get_DB_Struct_ToString('create_taskInfo') + ')'
    print(create_taskInfo)
    return create_taskInfo
# 用于初始化列表
def struct_taskInfo():
    struct_taskInfo = get_DB_Struct_ToString('struct_taskInfo')
    return struct_taskInfo


if __name__ == '__main__':
    print(getProjectPath())
    setProjectPath("./data/TestData")
    createProjectConfig()
    get_DB_Struct_ToString('struct_taskInfo')
    get_DB_Struct_ToString('create_taskInfo')
    get_DB_Struct_ToString('empty_taskInfo')
