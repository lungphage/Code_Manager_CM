<<<<<<< HEAD
# Code Manager v9.6

本地代码托管管理工具 - 支持 GitHub / Gitee 平台

## v9.6 更新内容

### Bug修复
- ✅ 修复新建配置时 `simpledialog` 未导入导致的崩溃
- ✅ 统一所有字体为 Segoe UI，UI风格一致

### v9.5 更新内容
=======
<<<<<<< HEAD
﻿# Code Manager v9.5

本地代码托管管理工具 - 支持 GitHub / Gitee 平台

## v9.5 更新内容

### UI美化（现代化风格）
>>>>>>> 7249cb9a7b20d00a0c4e65ec81790cbca4518779
- ✅ 采用 Segoe UI 字体，更现代的视觉效果
- ✅ 优化深色主题配色（GitHub Dark 风格）
- ✅ 增加控件间距和内边距，提升可读性
- ✅ Treeview 行高增加，更易点击
- ✅ 标签页样式优化
- ✅ 状态栏字体优化
<<<<<<< HEAD
- ✅ 窗口默认大小调整为 1280x860
=======
- ✅ 窗口默认大小调整

### 主题配色
- **浅色模式**: 更柔和的背景色，减少视觉疲劳
- **深色模式**: 采用 GitHub Dark 风格，护眼舒适
=======
<<<<<<< HEAD
﻿# Code Manager v9.4

本地代码托管管理工具 - 支持 GitHub / Gitee 平台

## v9.4 修复内容

### 修复推送失败问题
- ✅ 修复本地分支 master 与远程分支 main 不匹配问题
- ✅ 初始化时自动将分支重命名为 main
- ✅ 推送前自动检测并重命名分支
- ✅ 处理合并冲突（使用 -X theirs 策略）
- ✅ 推送前先提交更改

### 使用流程（新项目）
1. 选择本地项目文件夹
2. 输入远程仓库地址
3. 点击"初始化并关联（一键）"按钮
4. 点击"提交并推送"按钮
=======
﻿# Code Manager v8.0

本地代码托管管理工具 - 支持 GitHub / Gitee 平台
>>>>>>> 7249cb9a7b20d00a0c4e65ec81790cbca4518779

## 功能

- **上传代码**: 创建远程仓库并上传本地代码，支持选择开源协议
- **更新推送**: 提交更改并推送到远程仓库，支持拉取远程代码
- **分支管理**: 创建、切换、删除本地/远程分支
- **Fork仓库**: Fork他人仓库并克隆到本地
- **Release管理**: 创建Release并上传附件（仅GitHub）
- **仓库管理**: 查看和管理所有仓库信息
<<<<<<< HEAD
- **Issue/PR管理**: 创建、关闭Issue和PR
- **Webhook配置**: 配置仓库Webhook
- **搜索功能**: 搜索GitHub/Gitee上的开源仓库
- **统计面板**: 查看仓库统计数据
- **批量操作**: 批量上传、批量Fork
=======

## v8.0 更新内容

### 安全加固
- ✅ 使用Nuitka编译，源码保护大幅提升
- ✅ 反编译难度从⭐提升到⭐⭐⭐⭐
- ✅ 编译为机器码，运行速度略有提升

### v7.1 更新内容
- ✅ Release功能优化，创建前验证仓库
- ✅ 详细错误提示（404/422等）

### v7.0 更新内容
- ✅ 添加加载状态指示
- ✅ 危险操作确认对话框
- ✅ 输入格式验证
- ✅ 简化自定义主题
>>>>>>> 7249cb9a7b20d00a0c4e65ec81790cbca4518779

## 使用前准备

1. 安装 [Git](https://git-scm.com/)
2. 获取平台 Token:
<<<<<<< HEAD
   - **GitHub**: Settings → Developer settings → Personal access tokens (classic)，勾选 repo 权限
=======
   - **GitHub**: Settings → Developer settings → Personal access tokens (classic)，勾选 epo 权限
>>>>>>> 7249cb9a7b20d00a0c4e65ec81790cbca4518779
   - **Gitee**: 设置 → 私人令牌

## 运行方式

### 使用EXE（推荐）
<<<<<<< HEAD
```
dist/CodeManager_v9_6.exe
```

### 直接运行
```bash
pip install requests
python github_manager_v9.5.py
```

## 项目结构

```
v9.5/
├── .venv/                         # Python 3.12 虚拟环境
├── github_manager_v9.5.py         # 主程序 (v9.6.0)
├── build_nuitka.bat               # Nuitka构建脚本
├── README.md                      # 项目说明
├── 更新日志.txt                    # 版本记录
├── dist/
│   └── CodeManager_v9_6.exe       # Nuitka版（38.85MB）
├── icon.ico
├── icon.png
└── weixin.png
```
=======
`
dist/CodeManager_v8_0.exe
`

### 直接运行
`ash
pip install requests
python github_manager_v8.py
`

### 打包为EXE

#### Nuitka版本（推荐，更安全）
`ash
cd v8
build_nuitka.bat
`

#### PyInstaller版本（快速）
`ash
cd v8
build.bat
`

## 项目结构

`
v8/
├── .venv/                         # Python 3.12 虚拟环境
├── github_manager_v8.py           # 主程序 (v8.0.0)
├── build_nuitka.bat               # Nuitka构建脚本
├── build.bat                      # PyInstaller构建脚本
├── test_release.py                # Release测试脚本
├── README.md                      # 项目说明
├── 更新日志.txt                    # 版本记录
├── dist/
│   └── CodeManager_v8_0.exe       # Nuitka版（加壳保护，35MB）
├── icon.ico
├── icon.png
└── weixin.png
`

## 版本对比

| 项目 | PyInstaller版 | Nuitka版 |
|------|--------------|----------|
| 文件大小 | ~15MB | ~35MB |
| 反编译难度 | ⭐ 极易 | ⭐⭐⭐⭐ 很难 |
| 启动速度 | 快 | 更快 |
| 编译时间 | 30秒 | 5-10分钟 |

## 支持的开源协议

MIT, Apache 2.0, GPL v3, GPL v2, BSD 3-Clause, BSD 2-Clause, MPL 2.0, Unlicense, ISC, AGPL v3, CC0 1.0, EPL 2.0, LGPL 2.1
>>>>>>> 9f1342512d62e0ee06fa527768887d64140cb558
>>>>>>> f62eff4bc9cac51c13060ce3ab3c90497d3cb6aa
>>>>>>> 7249cb9a7b20d00a0c4e65ec81790cbca4518779

## 开发信息

- **作者**: LZF
<<<<<<< HEAD
- **版本**: 9.6.0
- **Python**: 3.12 (Nuitka编译)
=======
<<<<<<< HEAD
- **版本**: 9.5.0
- **Python**: 3.12 (Nuitka编译)
=======
<<<<<<< HEAD
- **版本**: 9.4.0
- **Python**: 3.12 (Nuitka编译)
=======
- **版本**: 8.0.0
- **Python**: 3.12 (Nuitka编译)
- **依赖**: requests, nuitka
- **打包**: Nuitka (推荐) / PyInstaller
>>>>>>> 9f1342512d62e0ee06fa527768887d64140cb558
>>>>>>> f62eff4bc9cac51c13060ce3ab3c90497d3cb6aa
>>>>>>> 7249cb9a7b20d00a0c4e65ec81790cbca4518779
