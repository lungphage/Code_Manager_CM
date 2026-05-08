# Code Manager v8.0

本地代码托管管理工具 - 支持 GitHub / Gitee 平台

## 功能

- **上传代码**: 创建远程仓库并上传本地代码，支持选择开源协议
- **更新推送**: 提交更改并推送到远程仓库，支持拉取远程代码
- **分支管理**: 创建、切换、删除本地/远程分支
- **Fork仓库**: Fork他人仓库并克隆到本地
- **Release管理**: 创建Release并上传附件（仅GitHub）
- **仓库管理**: 查看和管理所有仓库信息

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

## 使用前准备

1. 安装 [Git](https://git-scm.com/)
2. 获取平台 Token:
   - **GitHub**: Settings → Developer settings → Personal access tokens (classic)，勾选 epo 权限
   - **Gitee**: 设置 → 私人令牌

## 运行方式

### 使用EXE（推荐）
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

## 开发信息

- **作者**: LZF
- **版本**: 8.0.0
- **Python**: 3.12 (Nuitka编译)
- **依赖**: requests, nuitka
- **打包**: Nuitka (推荐) / PyInstaller
