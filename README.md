# Code Manager v10.2

本地代码托管管理工具 - 支持 GitHub / Gitee 平台

## v10.2 更新内容

### UI调整
- ✅ 操作日志面板移回右侧竖向显示

### v10.1 Bug修复
- ✅ 修复侧边栏Logo图标被截断问题
- ✅ 修复深色模式不完整，切换深色/浅色时全局UI完全重建
- ✅ 修复浅色模式下部分文字残留深色模式白色的问题

### v10.0 全新UI设计
- ✅ 全新Modern扁平化UI设计（Vercel/Notion风格）
- ✅ 侧边栏导航替代顶部标签页（Emoji图标 + 选中指示器 + hover效果）
- ✅ 卡片式容器布局（圆角边框 + 阴影效果）
- ✅ 渐变色按钮组件（Canvas绘制 + hover变亮）
- ✅ 自定义美化提示框（ToolTip组件）
- ✅ 新增Modern主题配色（蓝紫渐变，支持深色/浅色）

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
dist/CodeManager_v10_2.exe
```

### macOS（使用GitHub Actions构建）

1. Fork本仓库到你的GitHub账号
2. 进入仓库的 Actions 页面
3. 选择 "Build macOS App" 工作流
4. 点击 "Run workflow" 运行
5. 等待构建完成后，在 Artifacts 中下载 macOS 版本

### macOS（本地构建）
```bash
cd v10.2
chmod +x build_macos.sh
./build_macos.sh
```

### 直接运行
```bash
pip install requests
python github_manager_v10.2.py
```

## 构建说明

### Windows 构建
```bash
cd v10.2
build_nuitka.bat
```

### macOS 构建（通过GitHub Actions）

本项目配置了 GitHub Actions 自动构建 macOS 版本：

1. **自动触发**: 推送 `v*` 标签时自动构建
2. **手动触发**: 在 Actions 页面手动运行工作流
3. **下载产物**: 构建完成后在 Artifacts 中下载

```bash
# 创建标签并推送触发构建
git tag v10.2.0
git push origin v10.2.0
```

### macOS 构建（本地）

需要在 macOS 系统上运行：
```bash
cd v10.2
chmod +x build_macos.sh
./build_macos.sh
```

## 项目结构

```
v10.2/
├── .github/
│   └── workflows/
│       └── build-macos.yml    # GitHub Actions 工作流
├── github_manager_v10.2.py    # 主程序 (v10.2.0)
├── build_nuitka.bat           # Windows构建脚本
├── build_macos.sh             # macOS构建脚本
├── README.md                  # 项目说明
├── 更新日志.txt               # 版本记录
├── LICENSE                    # 开源协议
└── dist/
    └── CodeManager_v10_2.exe  # Windows版（39.3MB）
```

## 开发信息

- **作者**: LZF
- **版本**: 10.2.0
- **Python**: 3.12 (Nuitka编译)
- **支持平台**: Windows, macOS, Linux