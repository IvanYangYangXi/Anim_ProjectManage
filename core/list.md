# TaskList

- [ ] ~~ treeview 缩进设置（右键菜单）~~
- [x] 缩略图显示
- [x] 类型／状态关联图标- 类型存储为列表，存在 ProjectConfig 中
- [x] 新建项时创建文件夹
- [x] 详细信息面板 UI
- [x] 点击 item 展开子项
- [x] 加载下 2 级
- [x] 刷新重新加载
- [ ] 根项自动生成 资产 镜头
- [x] 双击 item 加载 详细信息面板 UI
- [x] 设置 详细信息
- [x] 提供数据类型选择
- [x] 根据数据类型设置 树和详细信息 ui 类型
- [x] 列表项数据更新时刷新 详细信息
- [x] 描述框大小
- [x] 细节面板缩略图
- [x] 详细面板 版本选项卡改为 文件
- [x] 如果没有缩略图点击选择缩略图
- [x] 缩略图添加右键菜单
- [x] 将 详细面板 的信息改动应用到 树列表
  - [x] 更新图片
  - [x] 任务名称
  - [x] 确定的 item 部件
  - [x] 动态添加的 item 部件
- [x] DB 数据添加英文名 （添加英文格式）
- [ ] 拖动文件到详细面板提交文件到对应目录
  - [x] 拖入释放文件，获取文件 path，name
  - [x] 判断名字是否符合规范 ( Type_StringName(\_SubName) ) ( Type: SM/SK/T/)
  - [x] 不符合规范->重命名,补全提示
  - [x] 检测是否有同名文件，有则创建历史版本文件
- [x] 自动重命名文件及历史版本，自动前缀后缀
- [ ] 为每个项创建目录
  - [x] 系统文件夹（ dbid/\$PMF_SystemFiles ）并设置文件夹为隐藏
  - [ ] 附件文件夹（ dbid/accessories ）
  - [x] 资产文件夹（ dbid/Content ）
  - [x] 历史版本文件（ dbid/Content/Revisions ）
  - [x] 自定义资产类型自动归类到对应文件夹下（默认分 sourceFile ：源文件（其他文件）， Meshes ：模型文件， Textures ：贴图文件）
- [x] 修改缩略图为指定目录下的图片（dbid/\$PMF_SystemFiles ）
- [ ] 选择或粘贴缩略图时自动复制到指定目录下
- [x] 根据标签获取 id
- [x] 文件目录／命名 统一化管理
- [x] 按类型显示文件
- [ ] 文件显示大小，修改时间，路径，审核状态
- [ ] 任务类型修改
- [ ] 添加文件审核清单
- [ ] 添加多层级审核流程

# Bug 记录

- [x] 详细信息面板 优先级 数据不更新
- [x] setFL_Info connect 混乱
- [ ] 树列表部件处于编辑状态时点击详细面板报错 in dataChangedAll if i.inherits('QSpinBox'):-AttributeError: 'int' object has no attribute 'inherits'
- [x] 细节面板 英文简称 项改变时 dataChangedAll 无触发 (QLineEdit 添加验证器后，editingFinished 事件不执行) -:验证器未满足，所以不触发添加验证器后，editingFinished

# 优化

- [ ] 下拉框字体大小、间距等
- [ ] 列表新建项、删除项的快捷键
- [ ] 设置列宽 TreeView ColumnWidth
- [ ] bug 点击箭头子项不更新
- [ ] 缩放界面时任务面板左侧栏固定宽度
- [x] 详细信息面板左侧添加长条状收缩按钮
