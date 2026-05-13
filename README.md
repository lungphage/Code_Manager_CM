# Code Manager v10.4

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
python github_manager_v10.4.py
```

### Windows EXE（无需安装 Python）

```
dist/CodeManager_v10_4.exe
```

---

## 构建 EXE

### Nuitka（推荐）

```bash
build_nuitka.bat
```

- 输出：`dist/CodeManager_v10_4.exe`（约 12MB，zstandard 压缩）
- 编译为原生二进制，启动快，代码受保护

### PyInstaller（备用）

```bash
build_pyinstaller.bat
```

- 输出：`dist/CodeManager_v10_4.exe`
- 安装简单，构建速度快

---

## 项目结构

```
v10.4/
├── github_manager_v10.4.py    # 主程序
├── build_nuitka.bat           # Nuitka 构建脚本（推荐）
├── build_pyinstaller.bat      # PyInstaller 构建脚本
├── CodeManager.spec           # PyInstaller spec 文件
├── README.md
├── 更新日志.txt
└── dist/
    └── CodeManager_v10_4.exe  # 打包输出（12MB）
```

---

## v10.4 优化内容

**性能优化**
- `GradientButton` 删除冗余的第一遍渐变绘制，新增颜色缓存，hover 响应更快

**Bug 修复**
- `PlatformAPI` 补全 `username` 属性，修复 Fork 后克隆时的 `AttributeError`
- `NetworkManager` 合并重复重试逻辑，修复连续限流后返回 `None` 导致的崩溃
- `list_repos` 缓存 `r.json()`，消除每次分页三次重复 JSON 解析
- 修复 EXE 启动崩溃：Token 迁移写入异常不再阻断启动流程

**封装改进**
- `GitOps` 新增 `pull_unrelated()` 和 `pull_with_strategy()` 方法，消除外部直接调用 `_run`

**代码质量**
- `App.log` 与 `_log_to_ui` 合并，线程安全逻辑统一到一处
- `_get_theme` 增加 `_normalize_theme`，统一补全各主题缺失的 fallback key
- 多处后台线程中的 StringVar/BooleanVar 读取移至主线程（`_do_upload`、`_do_commit`、`_do_push` 等）

**安全**
- Token 本地加密存储（机器绑定 XOR + base64），重启后无需重新输入
- 退出时只清内存，不再擦除磁盘上的加密 Token

---

## 开发信息

- **作者**：LZF
- **版本**：10.4.0
- **Python**：3.8+
- **依赖**：requests
- **打包**：Nuitka 4.x（主）/ PyInstaller 5.x（备）
