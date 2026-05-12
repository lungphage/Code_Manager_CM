# Code Manager v9.6

本地代码托管管理工具 - 支持 GitHub / Gitee 平台

## v9.6 更新内容

### Bug修复
- ✅ 修复新建配置时 `simpledialog` 未导入导致的崩溃
- ✅ 统一所有字体为 Segoe UI，UI风格一致

### 跨平台支持
- ✅ 新增 GitHub Actions 自动构建 macOS 版本
- ✅ 新增 macOS 本地构建脚本 `build_macos.sh`

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

### Windows（使用EXE）
```
dist/CodeManager_v9_6.exe
```

### macOS（使用GitHub Actions构建）

1. Fork本仓库到你的GitHub账号
2. 进入仓库的 Actions 页面
3. 选择 "Build macOS App" 工作流
4. 点击 "Run workflow" 运行
5. 等待构建完成后，在 Artifacts 中下载 macOS 版本

### macOS（本地构建）
```bash
cd v9.6
chmod +x build_macos.sh
./build_macos.sh
```

### 直接运行
```bash
pip install requests
python github_manager_v9.6.py
```

## 构建说明

### Windows 构建
```bash
cd v9.6
build_nuitka.bat
```

### macOS 构建（通过GitHub Actions）

本项目配置了 GitHub Actions 自动构建 macOS 版本：

1. **自动触发**: 推送 `v*` 标签时自动构建
2. **手动触发**: 在 Actions 页面手动运行工作流
3. **下载产物**: 构建完成后在 Artifacts 中下载

```bash
# 创建标签并推送触发构建
git tag v9.6.0
git push origin v9.6.0
```

### macOS 构建（本地）

需要在 macOS 系统上运行：
```bash
cd v9.6
chmod +x build_macos.sh
./build_macos.sh
```

## 项目结构

```
v9.6/
├── .github/
│   └── workflows/
│       └── build-macos.yml    # GitHub Actions 工作流
├── github_manager_v9.6.py     # 主程序 (v9.6.0)
├── build_nuitka.bat           # Windows构建脚本
├── build_macos.sh             # macOS构建脚本
├── README.md                  # 项目说明
├── 更新日志.txt                # 版本记录
└── dist/
    └── CodeManager_v9_6.exe   # Windows版（38.85MB）
```

## 开发信息

- **作者**: LZF
- **版本**: 9.6.0
- **Python**: 3.12 (Nuitka编译)
- **支持平台**: Windows, macOS, Linux
