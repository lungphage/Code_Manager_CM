# Code Manager v9.6

本地代码托管管理工具 - 支持 GitHub / Gitee 平台

## v9.6 更新内容

### Bug修复
- ✅ 修复新建配置时 `simpledialog` 未导入导致的崩溃
- ✅ 统一所有字体为 Segoe UI，UI风格一致

### v9.5 更新内容
- ✅ 采用 Segoe UI 字体，更现代的视觉效果
- ✅ 优化深色主题配色（GitHub Dark 风格）
- ✅ 增加控件间距和内边距，提升可读性
- ✅ Treeview 行高增加，更易点击
- ✅ 标签页样式优化
- ✅ 状态栏字体优化
- ✅ 窗口默认大小调整为 1280x860

## 功能

- **上传代码**: 创建远程仓库并上传本地代码，支持选择开源协议
- **更新推送**: 提交更改并推送到远程仓库，支持拉取远程代码
- **分支管理**: 创建、切换、删除本地/远程分支
- **Fork仓库**: Fork他人仓库并克隆到本地
- **Release管理**: 创建Release并上传附件（仅GitHub）
- **仓库管理**: 查看和管理所有仓库信息
- **Issue/PR管理**: 创建、关闭Issue和PR
- **Webhook配置**: 配置仓库Webhook
- **搜索功能**: 搜索GitHub/Gitee上的开源仓库
- **统计面板**: 查看仓库统计数据
- **批量操作**: 批量上传、批量Fork

## 使用前准备

1. 安装 [Git](https://git-scm.com/)
2. 获取平台 Token:
   - **GitHub**: Settings → Developer settings → Personal access tokens (classic)，勾选 repo 权限
   - **Gitee**: 设置 → 私人令牌

## 运行方式

### 使用EXE（推荐）
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

## 开发信息

- **作者**: LZF
- **版本**: 9.6.0
- **Python**: 3.12 (Nuitka编译)
