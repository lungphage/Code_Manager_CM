# Code Manager v10.3

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
python github_manager_v10.3.py
```

### Windows EXE（无需安装 Python）

```
dist/CodeManager_v10_3.exe
```

---

## 构建 EXE

### Nuitka（推荐）

```bash
build_nuitka.bat
```

- 输出：`dist/CodeManager_v10_3.exe`（约 12MB，zstandard 压缩）
- 编译为原生二进制，启动快，代码受保护

### PyInstaller（备用）

```bash
build_pyinstaller.bat
```

- 输出：`dist/CodeManager_v10_3.exe`
- 安装简单，构建速度快

---

## 项目结构

```
v10.3/
├── github_manager_v10.3.py    # 主程序
├── build_nuitka.bat           # Nuitka 构建脚本（推荐）
├── build_pyinstaller.bat      # PyInstaller 构建脚本
├── CodeManager.spec           # PyInstaller spec 文件
├── README.md
├── LICENSE
├── 更新日志.txt
└── dist/
    └── CodeManager_v10_3.exe  # 打包输出（12MB）
```

---

## v10.3 修复内容

**Bug 修复**
- 批量上传崩溃：`filedialog.askdirectories` 不存在，改为循环单选
- 设置页面崩溃：`StringVar.config()` 调用错误，改为保存 Combobox 实例
- 线程安全：分支/Fork 列表在后台线程直接操作控件，改为 `root.after(0, update)`
- 双重提交：`_do_commit_push` pull 前后各提交一次，整合为单次提交
- 日志轮转：`.1` 槽位从未创建，补充正确的文件重命名顺序

**安全加固**
- 导出配置时自动剥离 `token_*` 字段，防止凭据泄露
- 程序退出时将 token 删除持久化到磁盘
- 推送失败不再静默强制推送，改为提示用户手动确认

**构建优化**
- 引入 `zstandard` 压缩，EXE 体积从 40MB → **12MB**
- 修正废弃参数 `--windows-disable-console` → `--windows-console-mode=disable`

---

## 开发信息

- **作者**：LZF
- **版本**：10.3.0
- **Python**：3.8+
- **依赖**：requests
- **打包**：Nuitka 4.x（主）/ PyInstaller 5.x（备）
