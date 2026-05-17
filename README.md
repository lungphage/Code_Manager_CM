# Code Manager v10.5

本地代码托管管理工具，支持 GitHub / Gitee 双平台。

---

## 功能

| 模块 | 说明 |
|------|------|
| 上传代码 | 自动创建远程仓库、初始化 Git、关联并推送，支持开源协议与 .gitignore 模板 |
| 更新推送 | 提交本地修改并推送，支持拉取远程、强制推送、工作区状态查看 |
| 分支管理 | 创建/切换/删除本地与远程分支，远程分支列表展示 |
| Fork 仓库 | Fork 他人仓库并可自动克隆到本地，支持批量 Fork |
| Release | 创建 Release、上传附件（仅 GitHub） |
| 我的仓库 | 列出所有仓库，支持按语言/协议筛选、在浏览器打开、导出 CSV/JSON |
| 搜索 | 搜索 GitHub / Gitee 上的公开仓库 |
| Issue / PR | 创建、关闭 Issue 与 Pull Request |
| Webhook | 配置、测试、删除仓库 Webhook |
| 统计 | 仓库总数、Star/Fork 总量、语言分布、最近更新列表 |
| 设置 | 代理、超时、多配置文件管理、导入/导出配置 |

---

## 使用前准备

1. 安装 [Git](https://git-scm.com/)
2. 获取平台 Token：
   - **GitHub**：Settings → Developer settings → Personal access tokens (classic)，勾选 `repo` 权限
   - **Gitee**：设置 → 私人令牌

---

## 运行方式

### 直接运行（需 Python 3.8+）

```bash
pip install requests
python github_manager_v10.5.py
```

### Windows EXE（无需安装 Python）

```
dist/CodeManager_v10_5.exe
```

---

## 构建 EXE

### Nuitka（推荐）

```bash
build_nuitka.bat
```

- 输出：`dist/CodeManager_v10_5.exe`（约 12MB，zstandard 压缩）
- 编译为原生二进制，启动快，代码受保护

### PyInstaller（备用）

```bash
build_pyinstaller.bat
```

- 输出：`dist/CodeManager_v10_5.exe`
- 安装简单，构建速度快

---

## 项目结构

```
v10.5/
├── github_manager_v10.5.py    # 主程序
├── build_nuitka.bat           # Nuitka 构建脚本（推荐）
├── build_pyinstaller.bat      # PyInstaller 构建脚本
├── CodeManager.spec           # PyInstaller spec 文件
├── README.md
├── 更新日志.txt
└── dist/
    └── CodeManager_v10_5.exe  # 打包输出（12MB）
```

---

## v10.5 优化内容

**Bug 修复**
- 添加缺失的 `import base64`，修复 Token 加密/解密运行时崩溃
- `upload_release_asset` 改用 `NetworkManager`，恢复重试/代理/超时支持
- `os.startfile` 改为跨平台兼容（Windows/macOS/Linux）
- `_batch_upload` 分支从硬编码 "main" 改为读取用户设置
- `_show_loading` 的 `root.update()` 改为 `update_idletasks()` 防止事件循环重入

**代码重构**
- 提取 `_run_async` 辅助方法，消除 36 处线程模式重复代码（减少约 260 行）
- 提取 `_parse_owner_repo` 辅助方法，消除 18 处验证+拆分重复
- 提取 `_populate_treeview` 辅助方法，消除 8 处列表清空+填充重复

**代码清理**
- 删除未使用的 `import io`、`import ThreadPoolExecutor`
- 删除未使用的方法 `check_ssh()`、`get_submodules()`
- 提取 15 个命名常量替换魔法数字（超时、重试次数、分页大小等）
- 为 `PlatformAPI`、`GitOps`、`App` 的公共方法添加类型注解

---

## 开发信息

- **作者**：LZF
- **版本**：10.5.0
- **Python**：3.8+
- **依赖**：requests
- **打包**：Nuitka 4.x（主）/ PyInstaller 5.x（备）
