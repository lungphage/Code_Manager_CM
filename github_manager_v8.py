#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub/Gitee Manager v8.0 - 本地代码托管管理工具
Author: LZF
Version: 8.0.0
"""

__author__ = "LZF"
__version__ = "8.0.0"

import os
import sys
import json
import subprocess
import threading
import atexit
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, colorchooser
import webbrowser
import requests
from datetime import datetime

# ──────────────────────────── 路径与常量 ────────────────────────────

if getattr(sys, 'frozen', False):
    _BUNDLE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    BASE_DIR = os.path.dirname(sys.executable)
else:
    _BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = _BUNDLE_DIR

APP_NAME = "Code Manager"
APP_VERSION = __version__
APP_AUTHOR = __author__
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".github_manager_config.json")
ICON_PATH = os.path.join(_BUNDLE_DIR, "icon.png")
WEIXIN_PATH = os.path.join(_BUNDLE_DIR, "weixin.png")
GIT_DOWNLOAD_URL = "https://git-scm.com/download/win"

PLATFORMS = {
    "GitHub": {"api": "https://api.github.com", "web": "https://github.com", "token_note": "classic"},
    "Gitee":  {"api": "https://gitee.com/api/v5", "web": "https://gitee.com", "token_note": ""},
}

LICENSES = {
    "MIT License (MIT)": "mit",
    "Apache License 2.0": "apache-2.0",
    "GNU GPL v3.0": "gpl-3.0",
    "GNU GPL v2.0": "gpl-2.0",
    "BSD 3-Clause": "bsd-3-clause",
    "BSD 2-Clause": "bsd-2-clause",
    "Mozilla Public License 2.0": "mpl-2.0",
    "The Unlicense": "unlicense",
    "ISC License": "isc",
    "GNU AGPL v3.0": "agpl-3.0",
    "Creative Commons Zero v1.0": "cc0-1.0",
    "Eclipse Public License 2.0": "epl-2.0",
    "GNU LGPL v2.1": "lgpl-2.1",
    "不使用开源协议": ""
}

LICENSE_DESC = {
    "mit": "宽松许可，允许商用/修改/分发，需保留版权声明",
    "apache-2.0": "允许商用，含专利授权条款，需保留声明",
    "gpl-3.0": "强约束，衍生作品必须同样开源，禁止闭源使用",
    "gpl-2.0": "GPLv2，与v3类似但无额外专利保护",
    "bsd-3-clause": "宽松许可，禁止使用作者名做推广",
    "bsd-2-clause": "极简BSD，仅保留版权声明",
    "mpl-2.0": "文件级开源，修改的文件需开源，可与闭源组合",
    "unlicense": "完全放弃版权，等同公共领域",
    "isc": "极简宽松许可，类似MIT",
    "agpl-3.0": "GPLv3扩展，网络使用也需开源",
    "cc0-1.0": "公共领域贡献，无需署名",
    "epl-2.0": "Eclipse常用，允许商用，修改需开源",
    "lgpl-2.1": "允许链接使用，修改库本身需开源",
    "": "不添加开源协议，代码默认受版权保护"
}

# ──────────────────────────── 预设主题 ────────────────────────────

THEMES = {
    "微信(默认)": {
        "light": {
            "bg": "#f5f5f5", "bg2": "#ffffff", "bg3": "#ededed",
            "fg": "#333333", "fg2": "#666666", "fg3": "#999999",
            "accent": "#07c160", "accent_hover": "#06ad56",
            "header_bg": "#2e2e2e", "header_fg": "#ffffff",
            "btn_bg": "#07c160", "btn_fg": "#ffffff",
            "btn2_bg": "#ededed", "btn2_fg": "#333333",
            "entry_bg": "#ffffff", "entry_fg": "#333333",
            "select_bg": "#d4edda", "select_fg": "#333333",
            "log_bg": "#fafafa", "log_fg": "#333333",
            "tree_bg": "#ffffff", "tree_fg": "#333333",
            "tree_heading_bg": "#ededed",
            "border": "#e0e0e0",
            "tab_bg": "#e8e8e8", "tab_active": "#ffffff",
        },
        "dark": {
            "bg": "#1e1e1e", "bg2": "#2d2d2d", "bg3": "#252525",
            "fg": "#e0e0e0", "fg2": "#aaaaaa", "fg3": "#777777",
            "accent": "#07c160", "accent_hover": "#06ad56",
            "header_bg": "#1a1a1a", "header_fg": "#e0e0e0",
            "btn_bg": "#07c160", "btn_fg": "#ffffff",
            "btn2_bg": "#3a3a3a", "btn2_fg": "#e0e0e0",
            "entry_bg": "#2d2d2d", "entry_fg": "#e0e0e0",
            "select_bg": "#0a4a2a", "select_fg": "#e0e0e0",
            "log_bg": "#252525", "log_fg": "#cccccc",
            "tree_bg": "#2d2d2d", "tree_fg": "#e0e0e0",
            "tree_heading_bg": "#383838",
            "border": "#404040",
            "tab_bg": "#333333", "tab_active": "#2d2d2d",
        }
    },
    "VSCode": {
        "light": {
            "bg": "#f3f3f3", "bg2": "#ffffff", "bg3": "#efefef",
            "fg": "#333333", "fg2": "#616161", "fg3": "#999999",
            "accent": "#007acc", "accent_hover": "#0062a3",
            "header_bg": "#323233", "header_fg": "#ffffff",
            "btn_bg": "#007acc", "btn_fg": "#ffffff",
            "btn2_bg": "#efefef", "btn2_fg": "#333333",
            "entry_bg": "#ffffff", "entry_fg": "#333333",
            "select_bg": "#cce8ff", "select_fg": "#333333",
            "log_bg": "#fafafa", "log_fg": "#333333",
            "tree_bg": "#ffffff", "tree_fg": "#333333",
            "tree_heading_bg": "#efefef",
            "border": "#e0e0e0",
            "tab_bg": "#ececec", "tab_active": "#ffffff",
        },
        "dark": {
            "bg": "#1e1e1e", "bg2": "#252526", "bg3": "#2d2d2d",
            "fg": "#cccccc", "fg2": "#969696", "fg3": "#666666",
            "accent": "#007acc", "accent_hover": "#1a8ad4",
            "header_bg": "#323233", "header_fg": "#cccccc",
            "btn_bg": "#0e639c", "btn_fg": "#ffffff",
            "btn2_bg": "#3c3c3c", "btn2_fg": "#cccccc",
            "entry_bg": "#3c3c3c", "entry_fg": "#cccccc",
            "select_bg": "#094771", "select_fg": "#ffffff",
            "log_bg": "#1e1e1e", "log_fg": "#cccccc",
            "tree_bg": "#252526", "tree_fg": "#cccccc",
            "tree_heading_bg": "#2d2d2d",
            "border": "#404040",
            "tab_bg": "#2d2d2d", "tab_active": "#1e1e1e",
        }
    },
    "Cursor": {
        "light": {
            "bg": "#f7f7f8", "bg2": "#ffffff", "bg3": "#f0f0f2",
            "fg": "#2d2d30", "fg2": "#5c5c63", "fg3": "#9898a0",
            "accent": "#7c3aed", "accent_hover": "#6d28d9",
            "header_bg": "#2d2d30", "header_fg": "#ffffff",
            "btn_bg": "#7c3aed", "btn_fg": "#ffffff",
            "btn2_bg": "#f0f0f2", "btn2_fg": "#2d2d30",
            "entry_bg": "#ffffff", "entry_fg": "#2d2d30",
            "select_bg": "#ede9fe", "select_fg": "#2d2d30",
            "log_bg": "#fafafa", "log_fg": "#2d2d30",
            "tree_bg": "#ffffff", "tree_fg": "#2d2d30",
            "tree_heading_bg": "#f0f0f2",
            "border": "#e2e2e6",
            "tab_bg": "#eaeaed", "tab_active": "#ffffff",
        },
        "dark": {
            "bg": "#1a1a2e", "bg2": "#22223a", "bg3": "#1e1e32",
            "fg": "#e0e0ec", "fg2": "#a0a0b8", "fg3": "#6c6c84",
            "accent": "#7c3aed", "accent_hover": "#9061f0",
            "header_bg": "#16162a", "header_fg": "#e0e0ec",
            "btn_bg": "#7c3aed", "btn_fg": "#ffffff",
            "btn2_bg": "#2a2a44", "btn2_fg": "#e0e0ec",
            "entry_bg": "#2a2a44", "entry_fg": "#e0e0ec",
            "select_bg": "#3b2274", "select_fg": "#e0e0ec",
            "log_bg": "#1e1e32", "log_fg": "#ccccdd",
            "tree_bg": "#22223a", "tree_fg": "#e0e0ec",
            "tree_heading_bg": "#2a2a44",
            "border": "#3a3a54",
            "tab_bg": "#2a2a44", "tab_active": "#22223a",
        }
    }
}

CUSTOM_THEME_TEMPLATE = {
    "light": {
        "bg": "#f5f5f5", "bg2": "#ffffff", "bg3": "#ededed",
        "fg": "#333333", "fg2": "#666666", "fg3": "#999999",
        "accent": "#4a90d9", "accent_hover": "#3a7bc8",
        "header_bg": "#3a3a3a", "header_fg": "#ffffff",
        "btn_bg": "#4a90d9", "btn_fg": "#ffffff",
        "btn2_bg": "#ededed", "btn2_fg": "#333333",
        "entry_bg": "#ffffff", "entry_fg": "#333333",
        "select_bg": "#cce5ff", "select_fg": "#333333",
        "log_bg": "#fafafa", "log_fg": "#333333",
        "tree_bg": "#ffffff", "tree_fg": "#333333",
        "tree_heading_bg": "#ededed",
        "border": "#e0e0e0",
        "tab_bg": "#e8e8e8", "tab_active": "#ffffff",
    },
    "dark": {
        "bg": "#1e1e1e", "bg2": "#2d2d2d", "bg3": "#252525",
        "fg": "#e0e0e0", "fg2": "#aaaaaa", "fg3": "#777777",
        "accent": "#4a90d9", "accent_hover": "#5aa0e9",
        "header_bg": "#1a1a1a", "header_fg": "#e0e0e0",
        "btn_bg": "#4a90d9", "btn_fg": "#ffffff",
        "btn2_bg": "#3a3a3a", "btn2_fg": "#e0e0e0",
        "entry_bg": "#2d2d2d", "entry_fg": "#e0e0e0",
        "select_bg": "#1a3a5c", "select_fg": "#e0e0e0",
        "log_bg": "#252525", "log_fg": "#cccccc",
        "tree_bg": "#2d2d2d", "tree_fg": "#e0e0e0",
        "tree_heading_bg": "#383838",
        "border": "#404040",
        "tab_bg": "#333333", "tab_active": "#2d2d2d",
    }
}


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def mask_token(token):
    if not token or len(token) < 12:
        return "****"
    return token[:6] + "****" + token[-4:]


def check_git_installed():
    try:
        r = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=5)
        return r.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def validate_repo_name(name):
    """验证仓库名称格式"""
    import re
    if not name:
        return False, "仓库名称不能为空"
    if not re.match(r'^[a-zA-Z0-9._-]+$', name):
        return False, "仓库名称只能包含字母、数字、点、下划线和连字符"
    if len(name) > 100:
        return False, "仓库名称不能超过100个字符"
    return True, ""


def validate_branch_name(name):
    """验证分支名称格式"""
    import re
    if not name:
        return False, "分支名不能为空"
    if not re.match(r'^[a-zA-Z0-9._/-]+$', name):
        return False, "分支名只能包含字母、数字、点、下划线、连字符和斜杠"
    if '..' in name or name.startswith('.') or name.endswith('.'):
        return False, "分支名不能包含连续的点，也不能以点开头或结尾"
    return True, ""


def validate_owner_repo(text):
    """验证 owner/repo 格式"""
    if not text or '/' not in text:
        return False, "请输入格式：用户名/仓库名"
    parts = text.split('/', 1)
    if not parts[0] or not parts[1]:
        return False, "用户名和仓库名都不能为空"
    return True, ""


# ──────────────────────────── 平台 API ────────────────────────────

class PlatformAPI:
    def __init__(self, platform, token):
        self.platform = platform
        self.base = PLATFORMS[platform]["api"]
        self.web = PLATFORMS[platform]["web"]
        self.is_github = (platform == "GitHub")

        if self.is_github:
            self.headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
        else:
            self.headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        self._token = token

    def _req(self, method, url, **kwargs):
        kwargs.setdefault("headers", self.headers)
        return requests.request(method, url, **kwargs)

    def get_user(self):
        r = self._req("GET", f"{self.base}/user")
        if r.status_code == 200:
            d = r.json()
            if self.is_github:
                return d
            return {"login": d.get("login") or d.get("name", ""), "email": d.get("email", "N/A")}
        return None

    def list_repos(self):
        repos, page = [], 1
        while True:
            params = {"per_page": 100, "page": page, "sort": "updated"}
            if not self.is_github:
                params["type"] = "all"
            r = self._req("GET", f"{self.base}/user/repos", params=params)
            if r.status_code != 200 or not r.json():
                break
            repos.extend(r.json())
            page += 1
            if self.is_github and len(r.json()) < 100:
                break
        return repos

    def create_repo(self, name, desc="", private=False, license_key="", auto_init=True):
        data = {"name": name, "description": desc, "private": private, "auto_init": auto_init}
        if license_key:
            if self.is_github:
                data["license_template"] = license_key
            else:
                data["license"] = license_key
        return self._req("POST", f"{self.base}/user/repos", json=data)

    def get_repo(self, owner, repo):
        return self._req("GET", f"{self.base}/repos/{owner}/{repo}")

    def fork_repo(self, owner, repo):
        return self._req("POST", f"{self.base}/repos/{owner}/{repo}/forks")

    def list_branches(self, owner, repo):
        r = self._req("GET", f"{self.base}/repos/{owner}/{repo}/branches")
        return r.json() if r.status_code == 200 else []

    def create_branch(self, owner, repo, new_branch, sha):
        if self.is_github:
            return self._req("POST", f"{self.base}/repos/{owner}/{repo}/git/refs",
                             json={"ref": f"refs/heads/{new_branch}", "sha": sha})
        else:
            return self._req("POST", f"{self.base}/repos/{owner}/{repo}/branches",
                             json={"branch_name": new_branch, "ref": sha})

    def delete_branch(self, owner, repo, branch):
        return self._req("DELETE", f"{self.base}/repos/{owner}/{repo}/branches/{branch}")

    def get_branch_sha(self, owner, repo, branch):
        if self.is_github:
            r = self._req("GET", f"{self.base}/repos/{owner}/{repo}/git/refs/heads/{branch}")
            return r.json()["object"]["sha"] if r.status_code == 200 else None
        else:
            r = self._req("GET", f"{self.base}/repos/{owner}/{repo}/branches/{branch}")
            return r.json()["commit"]["sha"] if r.status_code == 200 else None

    def list_releases(self, owner, repo):
        if not self.is_github:
            r = self._req("GET", f"{self.base}/repos/{owner}/{repo}/releases")
            return r.json() if r.status_code == 200 else []
        r = self._req("GET", f"{self.base}/repos/{owner}/{repo}/releases")
        return r.json() if r.status_code == 200 else []

    def create_release(self, owner, repo, tag, name="", body="", draft=False, prerelease=False):
        data = {"tag_name": tag, "name": name or tag, "body": body, "draft": draft, "prerelease": prerelease}
        return self._req("POST", f"{self.base}/repos/{owner}/{repo}/releases", json=data)

    def upload_release_asset(self, upload_url, file_path, content_type="application/octet-stream"):
        if self.is_github:
            url = upload_url.split("{")[0]
            params = {"name": os.path.basename(file_path)}
            headers = {"Authorization": self.headers["Authorization"], "Content-Type": content_type}
            with open(file_path, "rb") as f:
                return requests.post(url, params=params, headers=headers, data=f)
        else:
            return None

    def get_clone_url(self, repo_data):
        if self.is_github:
            return repo_data.get("clone_url", "")
        url = repo_data.get("clone_url", "") or repo_data.get("html_url", "")
        if url.endswith(".git"):
            return url
        return url.rstrip("/") + ".git"

    def get_html_url(self, repo_data):
        return repo_data.get("html_url", "")


# ──────────────────────────── Git 操作 ────────────────────────────

class GitOps:
    def __init__(self, log_fn=None):
        self.log_fn = log_fn or print
        self._safe_dirs = set()

    def _add_safe_dir(self, path):
        abs_path = os.path.abspath(path)
        if abs_path not in self._safe_dirs:
            subprocess.run(["git", "config", "--global", "--add", "safe.directory", abs_path],
                           capture_output=True, timeout=10)
            self._safe_dirs.add(abs_path)

    def _run(self, args, cwd=None):
        try:
            r = subprocess.run(["git"] + args, cwd=cwd, capture_output=True,
                               text=True, encoding="utf-8", errors="replace", timeout=120)
            output = (r.stdout or "") + (r.stderr or "")
            if "dubious ownership" in output and cwd:
                self.log_fn("检测到文件系统所有权问题，自动修复中...")
                self._add_safe_dir(cwd)
                r = subprocess.run(["git"] + args, cwd=cwd, capture_output=True,
                                   text=True, encoding="utf-8", errors="replace", timeout=120)
            if r.stdout.strip():
                self.log_fn(r.stdout.strip())
            if r.stderr.strip():
                self.log_fn(r.stderr.strip())
            return r.returncode == 0, r.stdout, r.stderr
        except FileNotFoundError:
            self.log_fn("错误：未找到git命令")
            return False, "", "git not found"
        except subprocess.TimeoutExpired:
            self.log_fn("错误：git命令执行超时")
            return False, "", "timeout"
        except Exception as e:
            self.log_fn(f"错误：{e}")
            return False, "", str(e)

    def is_repo(self, path):
        return os.path.isdir(os.path.join(path, ".git"))

    def init(self, path):
        self.log_fn(f"git init → {path}")
        return self._run(["init"], cwd=path)

    def set_user_info(self, path, name, email):
        self._run(["config", "user.name", name], cwd=path)
        self._run(["config", "user.email", email], cwd=path)

    def has_commits(self, path):
        ok, out, _ = self._run(["rev-parse", "HEAD"], cwd=path)
        return ok

    def ensure_branch(self, path, target_branch):
        """确保当前分支名为target_branch，空仓库则先commit再rename"""
        current = self.current_branch(path)
        if current == target_branch:
            return True
        if not self.has_commits(path):
            self.add_all(path)
            self.commit(path, "Initial commit")
            current = self.current_branch(path)
        if current and current != target_branch:
            self.log_fn(f"重命名分支 {current} → {target_branch}")
            self.rename_branch(path, current, target_branch)
        return True

    def remote(self, path, url, name="origin"):
        ok, _, _ = self._run(["remote", "get-url", name], cwd=path)
        if ok:
            return self._run(["remote", "set-url", name, url], cwd=path)
        return self._run(["remote", "add", name, url], cwd=path)

    def add_all(self, path):
        return self._run(["add", "-A"], cwd=path)

    def commit(self, path, msg):
        self.log_fn(f'git commit -m "{msg}"')
        return self._run(["commit", "-m", msg], cwd=path)

    def push(self, path, remote="origin", branch="main", force=False):
        args = ["push", "-u", remote, branch]
        if force:
            args.insert(1, "--force")
        return self._run(args, cwd=path)

    def pull(self, path, remote="origin", branch="main"):
        return self._run(["pull", remote, branch], cwd=path)

    def checkout(self, path, branch, create=False):
        args = ["checkout", "-b", branch] if create else ["checkout", branch]
        return self._run(args, cwd=path)

    def current_branch(self, path):
        ok, out, _ = self._run(["rev-parse", "--abbrev-ref", "HEAD"], cwd=path)
        return out.strip() if ok else None

    def rename_branch(self, path, old_name, new_name):
        return self._run(["branch", "-m", old_name, new_name], cwd=path)

    def status(self, path):
        ok, out, _ = self._run(["status", "--porcelain"], cwd=path)
        return out.strip() if ok else ""

    def log(self, path, n=10):
        ok, out, _ = self._run(["log", "--oneline", f"-{n}"], cwd=path)
        return out.strip() if ok else ""

    def clone(self, url, path):
        return self._run(["clone", url, path])


# ──────────────────────────── 主应用 ────────────────────────────

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("1100x740")
        self.root.minsize(920, 660)

        self.cfg = load_config()
        self.api = None
        self.user = None
        self.git = GitOps(log_fn=self.log)
        self._repos_cache = self.cfg.get("local_repos", [])

        self.platform = self.cfg.get("platform", "GitHub")
        self.theme_name = self.cfg.get("theme", "微信(默认)")
        self.dark_mode = self.cfg.get("dark_mode", False)
        self.font_size = self.cfg.get("font_size", 9)
        self.custom_colors = self.cfg.get("custom_colors", CUSTOM_THEME_TEMPLATE.copy())

        self._icon_img = None
        self._weixin_img = None
        self._icon_small = None
        self._weixin_small = None
        self._load_images()
        self._apply_theme()
        self._build_ui()
        self._auto_login()
        self._check_git()

    def _load_images(self):
        try:
            if os.path.exists(ICON_PATH):
                img = tk.PhotoImage(file=ICON_PATH)
                self._icon_img = img
                self._icon_small = img.subsample(max(1, img.width() // 80), max(1, img.height() // 80))
        except Exception:
            pass
        try:
            if os.path.exists(WEIXIN_PATH):
                img = tk.PhotoImage(file=WEIXIN_PATH)
                self._weixin_img = img
                self._weixin_small = img.subsample(max(1, img.width() // 160), max(1, img.height() // 160))
        except Exception:
            pass

    def _get_theme(self):
        if self.theme_name == "自定义":
            t = self.custom_colors
            return t["dark"] if self.dark_mode else t["light"]
        t = THEMES.get(self.theme_name, THEMES["微信(默认)"])
        return t["dark"] if self.dark_mode else t["light"]

    def _apply_theme(self):
        t = self._get_theme()
        self._current_theme = t
        s = ttk.Style()
        try:
            s.theme_use("clam")
        except Exception:
            pass

        fs = self.font_size
        fsb = fs + 1
        fsh = fs + 4

        s.configure(".", background=t["bg"], foreground=t["fg"], font=("Microsoft YaHei UI", fs))
        s.configure("TFrame", background=t["bg"])
        s.configure("TLabel", background=t["bg"], foreground=t["fg"], font=("Microsoft YaHei UI", fs))
        s.configure("TButton", background=t["btn2_bg"], foreground=t["btn2_fg"],
                     font=("Microsoft YaHei UI", fs), padding=(10, 4), relief="flat")
        s.map("TButton",
               background=[("active", t["accent"]), ("pressed", t["accent_hover"])],
               foreground=[("active", t["btn_fg"]), ("pressed", t["btn_fg"])])

        s.configure("Accent.TButton", background=t["btn_bg"], foreground=t["btn_fg"],
                     font=("Microsoft YaHei UI", fsb, "bold"), padding=(14, 5), relief="flat")
        s.map("Accent.TButton",
               background=[("active", t["accent_hover"]), ("pressed", t["accent"])],
               foreground=[("active", t["btn_fg"])])

        s.configure("Header.TFrame", background=t["header_bg"])
        s.configure("Header.TLabel", background=t["header_bg"], foreground=t["header_fg"],
                     font=("Microsoft YaHei UI", fsh, "bold"))
        s.configure("Settings.TFrame", background=t["header_bg"])
        s.configure("Settings.TLabel", background=t["header_bg"], foreground=t["header_fg"],
                     font=("Microsoft YaHei UI", fs))
        s.configure("Theme.TButton", background=t["header_bg"], foreground=t["header_fg"],
                     font=("Microsoft YaHei UI", fs), padding=(6, 2), relief="flat")
        s.map("Theme.TButton",
               background=[("active", t["accent"])],
               foreground=[("active", "#ffffff")])

        s.configure("TNotebook", background=t["bg"], padding=2)
        s.configure("TNotebook.Tab", background=t["tab_bg"], foreground=t["fg"],
                     padding=(16, 6), font=("Microsoft YaHei UI", fs), relief="flat")
        s.map("TNotebook.Tab",
               background=[("selected", t["tab_active"])],
               foreground=[("selected", t["fg"])])

        s.configure("TEntry", fieldbackground=t["entry_bg"], foreground=t["entry_fg"],
                     insertcolor=t["entry_fg"], font=("Microsoft YaHei UI", fs), relief="flat")
        s.configure("TCombobox", fieldbackground=t["entry_bg"], foreground=t["entry_fg"],
                     font=("Microsoft YaHei UI", fs), relief="flat")

        s.configure("TLabelframe", background=t["bg"], foreground=t["fg"],
                     font=("Microsoft YaHei UI", fsb), relief="flat")
        s.configure("TLabelframe.Label", background=t["bg"], foreground=t["accent"],
                     font=("Microsoft YaHei UI", fsb, "bold"))

        s.configure("Treeview", background=t["tree_bg"], foreground=t["tree_fg"],
                     fieldbackground=t["tree_bg"], font=("Microsoft YaHei UI", fs), relief="flat")
        s.configure("Treeview.Heading", background=t["tree_heading_bg"], foreground=t["fg"],
                     font=("Microsoft YaHei UI", fsb), relief="flat")
        s.map("Treeview",
               background=[("selected", t["select_bg"])],
               foreground=[("selected", t["select_fg"])])

        s.configure("TSeparator", background=t["border"])
        s.configure("TRadiobutton", background=t["bg"], foreground=t["fg"], font=("Microsoft YaHei UI", fs))
        s.configure("TCheckbutton", background=t["bg"], foreground=t["fg"], font=("Microsoft YaHei UI", fs))
        s.configure("TScrollbar", background=t["bg3"], troughcolor=t["bg2"], arrowcolor=t["fg2"])

    def _rebuild_theme(self):
        self._apply_theme()
        t = self._current_theme
        self.root.configure(bg=t["bg"])
        for tw in [self.log_box, self.ud_status]:
            tw.configure(bg=t["log_bg"], fg=t["log_fg"], insertbackground=t["log_fg"],
                         selectbackground=t["select_bg"], font=("Consolas", self.font_size))
        for lb in [self.br_list, self.fk_list]:
            lb.configure(bg=t["tree_bg"], fg=t["tree_fg"], selectbackground=t["select_bg"],
                         selectforeground=t["select_fg"], font=("Consolas", self.font_size))
        self._update_status_bar()

    def _update_status_bar(self):
        """更新状态栏显示"""
        if hasattr(self, 'status_lbl'):
            self.status_lbl.config(text=f"v{APP_VERSION} | Author: {APP_AUTHOR} | 当前平台: {self.platform}")

    def _show_loading(self, message="处理中..."):
        """显示加载状态"""
        self.log(message)
        self.root.config(cursor="wait")
        self.root.update()

    def _hide_loading(self):
        """隐藏加载状态"""
        self.root.config(cursor="")

    def _confirm_dialog(self, title, message):
        """显示确认对话框"""
        return messagebox.askyesno(title, message, icon="warning")

    def _validate_and_run(self, validation_func, *args, **kwargs):
        """验证输入后执行操作"""
        is_valid, error_msg = validation_func(*args)
        if not is_valid:
            messagebox.showerror("输入错误", error_msg)
            return False
        return True

    # ─────────────────── UI 构建 ───────────────────

    def _build_ui(self):
        t = self._current_theme
        self.root.configure(bg=t["bg"])

        if self._icon_img:
            try:
                self.root.iconphoto(True, self._icon_img)
            except Exception:
                pass

        # 顶部栏
        hdr = ttk.Frame(self.root, style="Header.TFrame", padding=(12, 6))
        hdr.pack(fill=tk.X)

        self.user_lbl = ttk.Label(hdr, text="未登录", style="Header.TLabel")
        self.user_lbl.pack(side=tk.LEFT)

        ctrl = ttk.Frame(hdr, style="Settings.TFrame")
        ctrl.pack(side=tk.RIGHT)

        # 平台选择
        ttk.Label(ctrl, text="平台:", style="Settings.TLabel").pack(side=tk.LEFT, padx=(0, 2))
        self.platform_var = tk.StringVar(value=self.platform)
        plat_cb = ttk.Combobox(ctrl, textvariable=self.platform_var,
                                values=list(PLATFORMS.keys()), state="readonly", width=7)
        plat_cb.pack(side=tk.LEFT, padx=2)
        plat_cb.bind("<<ComboboxSelected>>", self._on_platform_change)

        ttk.Label(ctrl, text="主题:", style="Settings.TLabel").pack(side=tk.LEFT, padx=(8, 2))
        self.theme_var = tk.StringVar(value=self.theme_name)
        theme_cb = ttk.Combobox(ctrl, textvariable=self.theme_var,
                                 values=list(THEMES.keys()) + ["自定义"], state="readonly", width=10)
        theme_cb.pack(side=tk.LEFT, padx=2)
        theme_cb.bind("<<ComboboxSelected>>", self._on_theme_change)

        ttk.Label(ctrl, text="字号:", style="Settings.TLabel").pack(side=tk.LEFT, padx=(8, 2))
        self.font_var = tk.StringVar(value=str(self.font_size))
        font_cb = ttk.Combobox(ctrl, textvariable=self.font_var,
                                values=["8", "9", "10", "11", "12", "13", "14"], state="readonly", width=3)
        font_cb.pack(side=tk.LEFT, padx=2)
        font_cb.bind("<<ComboboxSelected>>", self._on_font_change)

        ttk.Label(ctrl, text="深色:", style="Settings.TLabel").pack(side=tk.LEFT, padx=(8, 2))
        self.dark_var = tk.BooleanVar(value=self.dark_mode)
        ttk.Checkbutton(ctrl, variable=self.dark_var, command=self._on_dark_toggle).pack(side=tk.LEFT, padx=2)

        ttk.Separator(ctrl, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=8, fill=tk.Y)
        ttk.Button(ctrl, text="Token设置", command=self._token_dlg, style="Theme.TButton").pack(side=tk.LEFT, padx=2)
        ttk.Button(ctrl, text="刷新", command=self._refresh, style="Theme.TButton").pack(side=tk.LEFT, padx=2)

        # 主体
        body = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        body.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))

        left = ttk.Frame(body)
        body.add(left, weight=3)

        self.nb = ttk.Notebook(left)
        self.nb.pack(fill=tk.BOTH, expand=True)

        self._tab_upload()
        self._tab_update()
        self._tab_branch()
        self._tab_fork()
        self._tab_release()
        self._tab_repos()
        self._tab_about()

        # 右侧日志
        rlf = ttk.LabelFrame(body, text=" 操作日志 ", padding=4)
        body.add(rlf, weight=2)
        t = self._current_theme
        self.log_box = scrolledtext.ScrolledText(rlf, wrap=tk.WORD, font=("Consolas", self.font_size),
                                                  relief=tk.FLAT, bg=t["log_bg"], fg=t["log_fg"],
                                                  insertbackground=t["log_fg"], selectbackground=t["select_bg"],
                                                  highlightthickness=0, bd=0)
        self.log_box.pack(fill=tk.BOTH, expand=True)
        ttk.Button(rlf, text="清空", command=lambda: self.log_box.delete("1.0", tk.END)).pack(anchor=tk.E, pady=(4, 0))

        # 底部状态栏
        status_bar = ttk.Frame(self.root, padding=(10, 2))
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_lbl = ttk.Label(status_bar, text=f"v{APP_VERSION} | Author: {APP_AUTHOR} | 当前平台: {self.platform}",
                                    foreground=t["fg3"], font=("Microsoft YaHei UI", 8))
        self.status_lbl.pack(side=tk.RIGHT)

    def _make_desc(self, parent, text, row=0, col=0, colspan=3):
        t = self._current_theme
        ttk.Label(parent, text=text, wraplength=580, justify=tk.LEFT,
                  foreground=t["fg2"], font=("Microsoft YaHei UI", self.font_size - 1)
                  ).grid(row=row, column=col, columnspan=colspan, sticky=tk.W, padx=4, pady=(0, 6))

    def _section_label(self, parent, text, row, col=0, colspan=3):
        t = self._current_theme
        ttk.Label(parent, text=text, font=("Microsoft YaHei UI", self.font_size, "bold"),
                  foreground=t["accent"]).grid(row=row, column=col, columnspan=colspan, sticky=tk.W, pady=(8, 2))

    # ─────────────────── 标签页：上传 ───────────────────

    def _tab_upload(self):
        f = ttk.Frame(self.nb, padding=12)
        self.nb.add(f, text="  上传代码  ")

        self._make_desc(f,
            "功能说明：将本地项目文件夹上传到GitHub/Gitee。自动创建新仓库，初始化Git，"
            "关联远程地址，提交所有文件并推送。首次上传时可选择开源协议（如MIT、Apache等），"
            "协议决定了他人使用你代码的权限。", 0)

        r = 1
        ttk.Label(f, text="本地项目路径：").grid(row=r, column=0, sticky=tk.W, pady=4)
        pf = ttk.Frame(f)
        pf.grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)
        self.up_path = tk.StringVar()
        ttk.Entry(pf, textvariable=self.up_path).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(pf, text="浏览…", width=7,
                   command=lambda: self._browse(self.up_path, auto_name=self.up_name)).pack(side=tk.LEFT, padx=4)

        r += 1
        ttk.Label(f, text="仓库名称：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.up_name = tk.StringVar()
        ttk.Entry(f, textvariable=self.up_name).grid(row=r, column=1, sticky=tk.EW, pady=4)

        r += 1
        ttk.Label(f, text="仓库描述：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.up_desc = tk.StringVar()
        ttk.Entry(f, textvariable=self.up_desc).grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)

        r += 1
        ttk.Label(f, text="可见性：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.up_priv = tk.BooleanVar(value=False)
        vf = ttk.Frame(f)
        vf.grid(row=r, column=1, sticky=tk.W, pady=4)
        ttk.Radiobutton(vf, text="公开 Public", variable=self.up_priv, value=False).pack(side=tk.LEFT)
        ttk.Radiobutton(vf, text="私有 Private", variable=self.up_priv, value=True).pack(side=tk.LEFT, padx=12)

        r += 1
        ttk.Label(f, text="开源协议：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.up_license = tk.StringVar(value="MIT License (MIT)")
        lc = ttk.Combobox(f, textvariable=self.up_license, values=list(LICENSES.keys()),
                          state="readonly", width=32)
        lc.grid(row=r, column=1, sticky=tk.W, pady=4)
        lc.bind("<<ComboboxSelected>>", self._license_hint)

        r += 1
        t = self._current_theme
        self.license_hint_lbl = ttk.Label(f, text="", foreground=t["fg2"],
                                           font=("Microsoft YaHei UI", self.font_size - 1), wraplength=500)
        self.license_hint_lbl.grid(row=r, column=1, columnspan=2, sticky=tk.W)

        r += 1
        ttk.Label(f, text="主分支名：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.up_branch = tk.StringVar(value="main")
        ttk.Entry(f, textvariable=self.up_branch, width=16).grid(row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        ttk.Label(f, text="提交信息：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.up_msg = tk.StringVar(value="Initial commit")
        ttk.Entry(f, textvariable=self.up_msg).grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)

        r += 1
        bf = ttk.Frame(f)
        bf.grid(row=r, column=0, columnspan=3, pady=14)
        ttk.Button(bf, text="创建仓库并上传", style="Accent.TButton", command=self._do_upload).pack(side=tk.LEFT, padx=6)
        ttk.Button(bf, text="仅创建远程仓库", command=self._do_create_repo).pack(side=tk.LEFT, padx=6)

        f.columnconfigure(1, weight=1)
        self._license_hint()

    def _license_hint(self, event=None):
        key = LICENSES.get(self.up_license.get(), "")
        desc = LICENSE_DESC.get(key, "")
        self.license_hint_lbl.config(text=desc)

    # ─────────────────── 标签页：更新 ───────────────────

    def _tab_update(self):
        f = ttk.Frame(self.nb, padding=12)
        self.nb.add(f, text="  更新推送  ")

        self._make_desc(f,
            "功能说明：对已关联远程仓库的本地项目进行日常更新。可以将本地修改提交（commit）"
            "并推送到远程仓库（push），也可以从远程拉取最新代码（pull）。"
            "支持查看当前工作区的文件变更状态和提交历史。", 0)

        r = 1
        ttk.Label(f, text="本地项目路径：").grid(row=r, column=0, sticky=tk.W, pady=4)
        pf = ttk.Frame(f)
        pf.grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)
        self.ud_path = tk.StringVar()
        ttk.Entry(pf, textvariable=self.ud_path).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(pf, text="浏览…", width=7, command=lambda: self._browse(self.ud_path)).pack(side=tk.LEFT, padx=4)

        r += 1
        ttk.Label(f, text="提交信息：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.ud_msg = tk.StringVar(value="Update")
        ttk.Entry(f, textvariable=self.ud_msg).grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)

        r += 1
        ttk.Label(f, text="远程分支：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.ud_branch = tk.StringVar(value="main")
        ttk.Entry(f, textvariable=self.ud_branch, width=16).grid(row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        self.ud_force = tk.BooleanVar(value=False)
        ttk.Checkbutton(f, text="强制推送（覆盖远程历史，慎用）", variable=self.ud_force).grid(
            row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        bf = ttk.Frame(f)
        bf.grid(row=r, column=0, columnspan=3, pady=10)
        ttk.Button(bf, text="提交并推送", style="Accent.TButton", command=self._do_commit_push).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="仅提交", command=self._do_commit).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="仅推送", command=self._do_push).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="拉取远程", command=self._do_pull).pack(side=tk.LEFT, padx=4)

        r += 1
        ttk.Separator(f, orient=tk.HORIZONTAL).grid(row=r, column=0, columnspan=3, sticky=tk.EW, pady=8)
        r += 1
        self._section_label(f, "工作区状态", r)
        r += 1
        t = self._current_theme
        self.ud_status = scrolledtext.ScrolledText(f, height=7, wrap=tk.WORD, font=("Consolas", self.font_size),
                                                    relief=tk.FLAT, bg=t["log_bg"], fg=t["log_fg"],
                                                    insertbackground=t["log_fg"], selectbackground=t["select_bg"],
                                                    highlightthickness=0, bd=0)
        self.ud_status.grid(row=r, column=0, columnspan=3, sticky=tk.EW, pady=4)
        r += 1
        ttk.Button(f, text="刷新状态", command=self._refresh_status).grid(row=r, column=0, sticky=tk.W, pady=4)
        f.columnconfigure(1, weight=1)

    # ─────────────────── 标签页：分支 ───────────────────

    def _tab_branch(self):
        f = ttk.Frame(self.nb, padding=12)
        self.nb.add(f, text="  分支管理  ")

        self._make_desc(f,
            "功能说明：管理Git分支。分支用于在不影响主线代码的情况下进行开发、测试或修复。"
            "可以从远程加载分支列表，创建新的本地/远程分支，切换当前分支，或删除不再需要的远程分支。"
            "常见用法：基于main创建dev分支进行开发。", 0)

        r = 1
        ttk.Label(f, text="本地项目路径：").grid(row=r, column=0, sticky=tk.W, pady=4)
        pf = ttk.Frame(f)
        pf.grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)
        self.br_path = tk.StringVar()
        ttk.Entry(pf, textvariable=self.br_path).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(pf, text="浏览…", width=7, command=lambda: self._browse(self.br_path)).pack(side=tk.LEFT, padx=4)

        r += 1
        ttk.Label(f, text="仓库地址 (owner/repo)：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.br_repo = tk.StringVar()
        ttk.Entry(f, textvariable=self.br_repo, width=28).grid(row=r, column=1, sticky=tk.EW, pady=4)
        ttk.Button(f, text="加载分支", command=self._load_branches).grid(row=r, column=2, padx=4, pady=4)

        r += 1
        self._section_label(f, "分支列表", r)
        r += 1
        lf = ttk.Frame(f)
        lf.grid(row=r, column=0, columnspan=3, sticky=tk.EW, pady=4)
        t = self._current_theme
        self.br_list = tk.Listbox(lf, height=7, font=("Consolas", self.font_size), relief=tk.FLAT,
                                   bg=t["tree_bg"], fg=t["tree_fg"],
                                   selectbackground=t["select_bg"], selectforeground=t["select_fg"],
                                   highlightthickness=0, bd=0)
        sb = ttk.Scrollbar(lf, orient=tk.VERTICAL, command=self.br_list.yview)
        self.br_list.configure(yscrollcommand=sb.set)
        self.br_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        r += 1
        ttk.Label(f, text="新分支名：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.br_new = tk.StringVar()
        ttk.Entry(f, textvariable=self.br_new, width=22).grid(row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        ttk.Label(f, text="基于分支：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.br_base = tk.StringVar(value="main")
        ttk.Entry(f, textvariable=self.br_base, width=16).grid(row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        bf = ttk.Frame(f)
        bf.grid(row=r, column=0, columnspan=3, pady=10)
        ttk.Button(bf, text="创建本地分支", command=self._br_local).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="创建远程分支", command=self._br_remote).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="切换到选中", command=self._br_switch).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="删除选中远程分支", command=self._br_delete).pack(side=tk.LEFT, padx=4)
        f.columnconfigure(1, weight=1)

    # ─────────────────── 标签页：Fork ───────────────────

    def _tab_fork(self):
        f = ttk.Frame(self.nb, padding=12)
        self.nb.add(f, text="  Fork仓库  ")

        self._make_desc(f,
            "功能说明：Fork（派生）他人的仓库到你自己的账号下。Fork后你会获得一份独立副本，"
            "可以在自己的副本上自由修改而不影响原仓库。常用于参与开源项目：Fork → 修改 → 提交PR。"
            '勾选"Fork后自动克隆"可直接将副本下载到本地。', 0)

        r = 1
        ttk.Label(f, text="目标仓库：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.fk_repo = tk.StringVar()
        ttk.Entry(f, textvariable=self.fk_repo, width=36).grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)
        t = self._current_theme
        ttk.Label(f, text="格式：用户名/仓库名", foreground=t["fg3"],
                  font=("Microsoft YaHei UI", self.font_size - 1)).grid(row=r, column=3, sticky=tk.W, padx=4)

        r += 1
        ttk.Label(f, text="克隆到本地：").grid(row=r, column=0, sticky=tk.W, pady=4)
        pf = ttk.Frame(f)
        pf.grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)
        self.fk_local = tk.StringVar()
        ttk.Entry(pf, textvariable=self.fk_local).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(pf, text="浏览…", width=7, command=lambda: self._browse_dir(self.fk_local)).pack(side=tk.LEFT, padx=4)

        r += 1
        self.fk_auto = tk.BooleanVar(value=True)
        ttk.Checkbutton(f, text="Fork后自动克隆到本地", variable=self.fk_auto).grid(row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        bf = ttk.Frame(f)
        bf.grid(row=r, column=0, columnspan=4, pady=10)
        ttk.Button(bf, text="Fork仓库", style="Accent.TButton", command=self._do_fork).pack(side=tk.LEFT, padx=6)
        ttk.Button(bf, text="仅克隆（已有Fork）", command=self._do_clone).pack(side=tk.LEFT, padx=6)

        r += 1
        ttk.Separator(f, orient=tk.HORIZONTAL).grid(row=r, column=0, columnspan=4, sticky=tk.EW, pady=8)
        r += 1
        self._section_label(f, "从仓库列表快速Fork", r)
        r += 1
        flf = ttk.Frame(f)
        flf.grid(row=r, column=0, columnspan=4, sticky=tk.EW, pady=4)
        self.fk_list = tk.Listbox(flf, height=8, font=("Consolas", self.font_size), relief=tk.FLAT,
                                   bg=t["tree_bg"], fg=t["tree_fg"],
                                   selectbackground=t["select_bg"], selectforeground=t["select_fg"],
                                   highlightthickness=0, bd=0)
        fsb = ttk.Scrollbar(flf, orient=tk.VERTICAL, command=self.fk_list.yview)
        self.fk_list.configure(yscrollcommand=fsb.set)
        self.fk_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        fsb.pack(side=tk.RIGHT, fill=tk.Y)

        r += 1
        bf2 = ttk.Frame(f)
        bf2.grid(row=r, column=0, columnspan=4, pady=4)
        ttk.Button(bf2, text="刷新列表", command=self._fk_load).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf2, text="Fork选中项", command=self._fk_selected).pack(side=tk.LEFT, padx=4)
        f.columnconfigure(1, weight=1)

    # ─────────────────── 标签页：Release ───────────────────

    def _tab_release(self):
        f = ttk.Frame(self.nb, padding=12)
        self.nb.add(f, text="  Release  ")

        self._make_desc(f,
            "功能说明：创建Release（发布版本），可将源代码打包或上传编译好的软件/文件作为附件。"
            "适用于正式发布版本、提供下载包、记录版本更新日志等场景。"
            "Tag名通常使用语义化版本号如 v1.0.0。"
            "注意：Gitee个人免费版不支持Release API，此功能仅限GitHub。", 0)

        r = 1
        ttk.Label(f, text="仓库地址 (owner/repo)：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.rl_repo = tk.StringVar()
        ttk.Entry(f, textvariable=self.rl_repo, width=36).grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)

        r += 1
        ttk.Label(f, text="Tag 名称：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.rl_tag = tk.StringVar(value="v1.0.0")
        ttk.Entry(f, textvariable=self.rl_tag, width=20).grid(row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        ttk.Label(f, text="Release 标题：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.rl_title = tk.StringVar()
        ttk.Entry(f, textvariable=self.rl_title).grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)

        r += 1
        ttk.Label(f, text="更新说明：").grid(row=r, column=0, sticky=tk.NW, pady=4)
        t = self._current_theme
        self.rl_body = scrolledtext.ScrolledText(f, height=5, wrap=tk.WORD, font=("Microsoft YaHei UI", self.font_size),
                                                  bg=t["entry_bg"], fg=t["entry_fg"],
                                                  insertbackground=t["entry_fg"], highlightthickness=0, bd=1, relief="solid")
        self.rl_body.grid(row=r, column=1, columnspan=3, sticky=tk.EW, pady=4)
        self.rl_body.insert("1.0", "## 更新内容\n\n- ")

        r += 1
        self.rl_draft = tk.BooleanVar(value=False)
        self.rl_pre = tk.BooleanVar(value=False)
        df = ttk.Frame(f)
        df.grid(row=r, column=1, sticky=tk.W, pady=4)
        ttk.Checkbutton(df, text="草稿 (Draft)", variable=self.rl_draft).pack(side=tk.LEFT)
        ttk.Checkbutton(df, text="预发布 (Pre-release)", variable=self.rl_pre).pack(side=tk.LEFT, padx=12)

        r += 1
        self._section_label(f, "附件上传（可选）", r)
        r += 1
        af = ttk.Frame(f)
        af.grid(row=r, column=0, columnspan=4, sticky=tk.EW, pady=4)
        self.rl_assets_var = tk.StringVar(value="")
        ttk.Entry(af, textvariable=self.rl_assets_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(af, text="选择文件…", width=9, command=self._browse_assets).pack(side=tk.LEFT, padx=4)
        ttk.Button(af, text="清空", width=5, command=lambda: self.rl_assets_var.set("")).pack(side=tk.LEFT, padx=2)

        r += 1
        ttk.Label(f, text="支持多文件，用分号 ; 分隔路径", foreground=t["fg3"],
                  font=("Microsoft YaHei UI", self.font_size - 1)).grid(row=r, column=1, sticky=tk.W)

        r += 1
        bf = ttk.Frame(f)
        bf.grid(row=r, column=0, columnspan=4, pady=14)
        ttk.Button(bf, text="创建 Release", style="Accent.TButton", command=self._do_release).pack(side=tk.LEFT, padx=6)
        ttk.Button(bf, text="查看已有 Release", command=self._list_releases).pack(side=tk.LEFT, padx=6)

        r += 1
        ttk.Separator(f, orient=tk.HORIZONTAL).grid(row=r, column=0, columnspan=4, sticky=tk.EW, pady=8)
        r += 1
        self._section_label(f, "已有 Release 列表", r)
        r += 1
        cols = ("Tag", "标题", "状态", "创建时间")
        self.rl_tree = ttk.Treeview(f, columns=cols, show="headings", height=8)
        for c in cols:
            self.rl_tree.heading(c, text=c)
        self.rl_tree.column("Tag", width=100)
        self.rl_tree.column("标题", width=200)
        self.rl_tree.column("状态", width=80, anchor=tk.CENTER)
        self.rl_tree.column("创建时间", width=120, anchor=tk.CENTER)
        self.rl_tree.grid(row=r, column=0, columnspan=4, sticky=tk.EW, pady=4)
        rsb = ttk.Scrollbar(f, orient=tk.VERTICAL, command=self.rl_tree.yview)
        self.rl_tree.configure(yscrollcommand=rsb.set)
        rsb.grid(row=r, column=4, sticky=tk.NS, pady=4)
        f.columnconfigure(1, weight=1)

    def _browse_assets(self):
        files = filedialog.askopenfilenames(title="选择要上传的文件")
        if files:
            self.rl_assets_var.set(";".join(files))

    def _do_release(self):
        if not self._need_auth():
            return
        if self.platform != "GitHub":
            messagebox.showinfo("提示", "Release功能目前仅支持GitHub平台")
            return
        rp = self.rl_repo.get().strip()
        
        # 验证 owner/repo 格式
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            messagebox.showerror("输入错误", error_msg)
            return
        
        tag = self.rl_tag.get().strip()
        if not tag:
            messagebox.showerror("错误", "请输入Tag名称")
            return
        
        # 验证Tag格式
        if not tag.startswith("v") and not tag[0].isdigit():
            messagebox.showwarning("提示", "Tag通常以'v'开头，如 v1.0.0")
        
        self._show_loading("正在创建Release...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                
                # 先验证仓库是否存在
                self.log(f"验证仓库 {rp} 是否存在...")
                repo_resp = self.api.get_repo(owner, repo)
                if repo_resp.status_code == 404:
                    self.log(f"错误：仓库 {rp} 不存在或无访问权限")
                    self.log("请检查：")
                    self.log("  1. 用户名/仓库名是否正确")
                    self.log("  2. 仓库是否为私有仓库（需要相应权限）")
                    self.log("  3. Token是否有访问该仓库的权限")
                    return
                elif repo_resp.status_code != 200:
                    self.log(f"验证仓库失败：{repo_resp.status_code}")
                    return
                
                self.log(f"仓库验证通过，开始创建Release...")
                title = self.rl_title.get().strip() or tag
                body = self.rl_body.get("1.0", tk.END).strip()
                self.log(f"正在创建 Release: {tag}...")
                resp = self.api.create_release(owner, repo, tag, title, body, self.rl_draft.get(), self.rl_pre.get())
                if resp.status_code == 201:
                    rd = resp.json()
                    self.log(f"Release 创建成功: {rd['html_url']}")
                    assets = self.rl_assets_var.get().strip()
                    if assets:
                        upload_url = rd.get("upload_url", "")
                        for fp in assets.split(";"):
                            fp = fp.strip()
                            if fp and os.path.isfile(fp):
                                self.log(f"上传附件: {os.path.basename(fp)}...")
                                ar = self.api.upload_release_asset(upload_url, fp)
                                if ar and ar.status_code == 201:
                                    self.log(f"  附件上传成功")
                                else:
                                    self.log(f"  附件上传失败: {ar.status_code if ar else '未知错误'}")
                    self.root.after(0, self._list_releases)
                elif resp.status_code == 404:
                    self.log(f"创建失败：无法创建Release，请检查仓库是否存在")
                    self.log("可能原因：")
                    self.log("  1. 仓库不存在")
                    self.log("  2. Token权限不足（需要repo权限）")
                    self.log("  3. Tag名称格式错误")
                elif resp.status_code == 422:
                    error_detail = resp.json().get("message", "")
                    self.log(f"创建失败：数据验证错误 - {error_detail}")
                    self.log("可能原因：")
                    self.log("  1. Tag名称已存在")
                    self.log("  2. Tag格式不符合规范")
                else:
                    self.log(f"创建失败: {resp.status_code}")
                    try:
                        error_info = resp.json()
                        self.log(f"错误信息: {error_info.get('message', '')}")
                    except:
                        self.log(f"响应内容: {resp.text[:200]}")
            except Exception as e:
                self.log(f"创建Release异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)

        threading.Thread(target=task, daemon=True).start()

    def _list_releases(self):
        if not self._need_auth():
            return
        rp = self.rl_repo.get().strip()
        
        # 验证 owner/repo 格式
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            return
        
        self._show_loading("正在加载Release列表...")

        def task():
            try:
                owner, repo = rp.split("/", 1)
                releases = self.api.list_releases(owner, repo)
                def update():
                    for i in self.rl_tree.get_children():
                        self.rl_tree.delete(i)
                    for r in releases:
                        status = "草稿" if r.get("draft") else ("预发布" if r.get("prerelease") else "正式")
                        created = (r.get("created_at") or "")[:10]
                        self.rl_tree.insert("", tk.END, values=(r.get("tag_name", ""), r.get("name", ""), status, created))
                self.root.after(0, update)
                self.log(f"加载了 {len(releases)} 个 Release")
            except Exception as e:
                self.log(f"加载Release列表失败：{e}")
            finally:
                self.root.after(0, self._hide_loading)

        threading.Thread(target=task, daemon=True).start()

    # ─────────────────── 标签页：我的仓库 ───────────────────

    def _tab_repos(self):
        f = ttk.Frame(self.nb, padding=12)
        self.nb.add(f, text="  我的仓库  ")

        self._make_desc(f,
            "功能说明：查看你账号下的所有仓库信息，包括名称、可见性、使用的开源协议、"
            "编程语言和最后更新时间。双击仓库可在浏览器中打开对应页面。", 0)

        r = 1
        bf = ttk.Frame(f)
        bf.grid(row=r, column=0, columnspan=3, sticky=tk.W, pady=4)
        ttk.Button(bf, text="刷新列表", command=self._repos_load).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="浏览器中打开选中仓库", command=self._repos_open).pack(side=tk.LEFT, padx=4)

        r += 1
        cols = ("仓库名称", "可见性", "开源协议", "语言", "最后更新")
        self.repo_tree = ttk.Treeview(f, columns=cols, show="headings", height=16)
        for c in cols:
            self.repo_tree.heading(c, text=c)
        self.repo_tree.column("仓库名称", width=220)
        self.repo_tree.column("可见性", width=60, anchor=tk.CENTER)
        self.repo_tree.column("开源协议", width=100, anchor=tk.CENTER)
        self.repo_tree.column("语言", width=80, anchor=tk.CENTER)
        self.repo_tree.column("最后更新", width=110, anchor=tk.CENTER)
        self.repo_tree.grid(row=r, column=0, columnspan=3, sticky=tk.EW, pady=4)
        rsb = ttk.Scrollbar(f, orient=tk.VERTICAL, command=self.repo_tree.yview)
        self.repo_tree.configure(yscrollcommand=rsb.set)
        rsb.grid(row=r, column=3, sticky=tk.NS, pady=4)
        self.repo_tree.bind("<Double-1>", lambda e: self._repos_open())
        f.columnconfigure(0, weight=1)

    # ─────────────────── 标签页：关于 ───────────────────

    def _tab_about(self):
        f = ttk.Frame(self.nb, padding=12)
        self.nb.add(f, text="  关于软件  ")
        t = self._current_theme

        if self._icon_small:
            ttk.Label(f, image=self._icon_small).grid(row=0, column=0, columnspan=2, pady=(10, 6))

        ttk.Label(f, text=f"{APP_NAME} v{APP_VERSION}",
                  font=("Microsoft YaHei UI", 14, "bold"),
                  foreground=t["accent"]).grid(row=1, column=0, columnspan=2, pady=4)

        ttk.Label(f, text="GitHub / Gitee 本地代码管理工具",
                  font=("Microsoft YaHei UI", 10),
                  foreground=t["fg2"]).grid(row=2, column=0, columnspan=2, pady=2)

        ttk.Separator(f, orient=tk.HORIZONTAL).grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=10)

        info_frame = ttk.Frame(f)
        info_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=20)

        ttk.Label(info_frame, text="开发者：", font=("Microsoft YaHei UI", 10, "bold"),
                  foreground=t["fg"]).grid(row=0, column=0, sticky=tk.W, pady=3)
        ttk.Label(info_frame, text=APP_AUTHOR, font=("Microsoft YaHei UI", 10),
                  foreground=t["fg"]).grid(row=0, column=1, sticky=tk.W, pady=3, padx=8)

        ttk.Label(info_frame, text="版本号：", font=("Microsoft YaHei UI", 10, "bold"),
                  foreground=t["fg"]).grid(row=1, column=0, sticky=tk.W, pady=3)
        ttk.Label(info_frame, text=f"v{APP_VERSION}", font=("Microsoft YaHei UI", 10),
                  foreground=t["fg"]).grid(row=1, column=1, sticky=tk.W, pady=3, padx=8)

        ttk.Separator(f, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=10)

        ttk.Label(f, text="联系方式 - 微信扫码添加好友",
                  font=("Microsoft YaHei UI", 11, "bold"),
                  foreground=t["accent"]).grid(row=6, column=0, columnspan=2, pady=(4, 6))

        if self._weixin_small:
            ttk.Label(f, image=self._weixin_small).grid(row=7, column=0, columnspan=2, pady=4)
        else:
            ttk.Label(f, text="[ 微信二维码图片未找到 ]", foreground=t["fg3"]).grid(row=7, column=0, columnspan=2, pady=4)

        f.columnconfigure(0, weight=1)

    # ─────────────────── 平台切换 ───────────────────

    def _on_platform_change(self, event=None):
        self.platform = self.platform_var.get()
        self.cfg["platform"] = self.platform
        save_config(self.cfg)
        self.api = None
        self.user = None
        self.user_lbl.config(text="未登录")
        self.log(f"已切换到 {self.platform} 平台，请重新设置Token")

    # ─────────────────── Git 检测 ───────────────────

    def _check_git(self):
        if not check_git_installed():
            self.log("警告：未检测到Git安装")
            if messagebox.askyesno("Git 未安装",
                                    "本软件需要 Git 才能正常工作。\n\n"
                                    "是否打开 Git 下载页面？\n"
                                    "下载安装后请重启本软件。"):
                webbrowser.open(GIT_DOWNLOAD_URL)

    # ─────────────────── 主题切换 ───────────────────

    def _on_theme_change(self, event=None):
        name = self.theme_var.get()
        if name == "自定义":
            self._open_color_picker()
            return
        self.theme_name = name
        self.cfg["theme"] = name
        save_config(self.cfg)
        self._rebuild_theme()

    def _on_font_change(self, event=None):
        try:
            self.font_size = int(self.font_var.get())
        except ValueError:
            return
        self.cfg["font_size"] = self.font_size
        save_config(self.cfg)
        self._rebuild_theme()

    def _on_dark_toggle(self):
        self.dark_mode = self.dark_var.get()
        self.cfg["dark_mode"] = self.dark_mode
        save_config(self.cfg)
        self._rebuild_theme()

    def _open_color_picker(self):
        t = self._current_theme
        d = tk.Toplevel(self.root)
        d.title("自定义配色方案")
        d.geometry("450x400")
        d.resizable(False, False)
        d.transient(self.root)
        d.grab_set()
        d.configure(bg=t["bg2"])

        mode = "dark" if self.dark_var.get() else "light"
        colors = self.custom_colors.get(mode, CUSTOM_THEME_TEMPLATE[mode])

        color_vars = {}
        # 简化：只保留最常用的颜色选项
        labels = {
            "bg": "主背景色",
            "fg": "主文字色",
            "accent": "强调色",
            "btn_bg": "按钮背景",
            "btn_fg": "按钮文字",
            "entry_bg": "输入框背景",
            "entry_fg": "输入框文字",
            "tree_bg": "列表背景",
            "tree_fg": "列表文字",
        }

        main_frame = ttk.Frame(d, padding=12)
        main_frame.pack(fill=tk.BOTH, expand=True)

        row = 0
        ttk.Label(main_frame, text="自定义配色（点击色块选择颜色）",
                  font=("Microsoft YaHei UI", 11, "bold"),
                  foreground=t["accent"]).grid(row=row, column=0, columnspan=3, pady=(0, 10))

        for key, label in labels.items():
            row += 1
            var = tk.StringVar(value=colors.get(key, "#ffffff"))
            color_vars[key] = var
            ttk.Label(main_frame, text=f"{label}：", width=12, anchor=tk.W).grid(row=row, column=0, sticky=tk.W, pady=4, padx=4)
            preview = tk.Frame(main_frame, width=28, height=20, bg=colors.get(key, "#ffffff"), relief="solid", bd=1)
            preview.grid(row=row, column=1, padx=4, pady=4)
            entry = ttk.Entry(main_frame, textvariable=var, width=12)
            entry.grid(row=row, column=2, padx=4, pady=4)

            def pick_color(v=var, p=preview, k=key):
                c = colorchooser.askcolor(color=v.get(), title=f"选择 {labels.get(k, k)}")
                if c and c[1]:
                    v.set(c[1])
                    p.configure(bg=c[1])

            ttk.Button(main_frame, text="选色", width=5, command=pick_color).grid(row=row, column=3, padx=4, pady=4)
            var.trace_add("write", lambda *a, v=var, p=preview: p.configure(bg=v.get()) if v.get().startswith("#") else None)

        def apply_custom():
            for key, var in color_vars.items():
                val = var.get().strip()
                if val.startswith("#") and len(val) == 7:
                    self.custom_colors[mode][key] = val
            self.cfg["custom_colors"] = self.custom_colors
            self.theme_name = "自定义"
            self.cfg["theme"] = "自定义"
            save_config(self.cfg)
            self.theme_var.set("自定义")
            self._rebuild_theme()
            d.destroy()

        bf = ttk.Frame(main_frame)
        bf.grid(row=row + 1, column=0, columnspan=4, pady=(16, 0))
        ttk.Button(bf, text="应用配色", style="Accent.TButton", command=apply_custom).pack(side=tk.RIGHT, padx=4)
        ttk.Button(bf, text="取消", command=d.destroy).pack(side=tk.RIGHT, padx=4)

    # ─────────────────── 认证 ───────────────────

    def _auto_login(self):
        token = self.cfg.get(f"token_{self.platform}", self.cfg.get("token", ""))
        if token:
            self._set_token(token)

    def _token_dlg(self):
        t = self._current_theme
        d = tk.Toplevel(self.root)
        d.title(f"{self.platform} Token 设置")
        d.geometry("540x220")
        d.resizable(False, False)
        d.transient(self.root)
        d.grab_set()
        d.configure(bg=t["bg2"])

        note = ""
        if self.platform == "GitHub":
            note = "获取路径：GitHub → Settings → Developer settings → Personal access tokens (classic)"
        else:
            note = "获取路径：Gitee → 设置 → 私人令牌"

        ttk.Label(d, text=f"{self.platform} Personal Access Token：",
                  font=("Microsoft YaHei UI", self.font_size + 1),
                  background=t["bg2"], foreground=t["fg"]).pack(padx=16, pady=(16, 4), anchor=tk.W)
        tv = tk.StringVar(value=self.cfg.get(f"token_{self.platform}", self.cfg.get("token", "")))
        ttk.Entry(d, textvariable=tv, width=58, show="•").pack(padx=16, fill=tk.X)
        ttk.Label(d, text=note, foreground=t["fg3"],
                  font=("Microsoft YaHei UI", self.font_size - 1),
                  background=t["bg2"]).pack(padx=16, pady=4, anchor=tk.W)

        def ok():
            token = tv.get().strip()
            if not token:
                messagebox.showwarning("提示", "请输入Token", parent=d)
                return
            self._set_token(token)
            self.cfg[f"token_{self.platform}"] = token
            save_config(self.cfg)
            d.destroy()

        ttk.Button(d, text="保存", style="Accent.TButton", command=ok).pack(pady=14)

    def _set_token(self, token):
        self.api = PlatformAPI(self.platform, token)
        u = self.api.get_user()
        if u:
            self.user = u
            self.user_lbl.config(text=f"[{self.platform}] 已登录：{u['login']}")
            self.log(f"认证成功：{u['login']} ({u.get('email', 'N/A')})")
            self.log(f"Token: {mask_token(token)}")
        else:
            self.user_lbl.config(text=f"[{self.platform}] 认证失败")
            self.log("Token认证失败，请检查Token是否正确或已过期")

    def _need_auth(self):
        if not self.api or not self.user:
            messagebox.showwarning("提示", f"请先设置{self.platform} Token")
            self._token_dlg()
            return False
        return True

    def _cleanup(self):
        for p in PLATFORMS:
            self.cfg.pop(f"token_{p}", None)
        self.cfg.pop("token", None)
        self.api = None
        self.user = None

    # ─────────────────── 文件浏览 ───────────────────

    def _browse(self, var, auto_name=None):
        p = filedialog.askdirectory(title="选择本地项目文件夹")
        if p:
            var.set(p)
            if auto_name and not auto_name.get():
                auto_name.set(os.path.basename(p))

    def _browse_dir(self, var):
        p = filedialog.askdirectory(title="选择目标文件夹")
        if p:
            var.set(p)

    # ─────────────────── 上传 ───────────────────

    def _do_upload(self):
        if not self._need_auth():
            return
        path = self.up_path.get().strip()
        name = self.up_name.get().strip()
        if not path or not os.path.isdir(path):
            messagebox.showerror("错误", "请选择有效的本地项目路径")
            return
        
        # 验证仓库名称
        is_valid, error_msg = validate_repo_name(name)
        if not is_valid:
            messagebox.showerror("输入错误", error_msg)
            return
        
        # 验证分支名
        branch = self.up_branch.get().strip() or "main"
        is_valid, error_msg = validate_branch_name(branch)
        if not is_valid:
            messagebox.showerror("输入错误", f"分支名无效：{error_msg}")
            return

        self._show_loading("正在创建仓库并上传...")

        def task():
            try:
                desc = self.up_desc.get().strip()
                priv = self.up_priv.get()
                lic = LICENSES.get(self.up_license.get(), "")
                target_branch = branch
                msg = self.up_msg.get().strip() or "Initial commit"

                self.log(f"正在创建远程仓库：{name}...")
                resp = self.api.create_repo(name, desc, priv, lic, auto_init=False)
                if resp.status_code == 201:
                    data = resp.json()
                    clone_url = self.api.get_clone_url(data)
                    html_url = self.api.get_html_url(data)
                    self.log(f"远程仓库创建成功：{html_url}")
                elif resp.status_code == 422:
                    self.log(f"仓库 {name} 已存在，将直接关联...")
                    data = self.api.get_repo(self.user["login"], name).json()
                    clone_url = self.api.get_clone_url(data)
                    html_url = self.api.get_html_url(data)
                else:
                    self.log(f"创建失败：{resp.status_code} {resp.text}")
                    self.root.after(0, self._hide_loading)
                    return

                if not self.git.is_repo(path):
                    self.git.init(path)

                # 设置用户信息（从平台API获取）
                username = self.user.get("login", "user")
                email = self.user.get("email") or f"{username}@users.noreply.com"
                if email == "N/A":
                    email = f"{username}@users.noreply.com"
                self.git.set_user_info(path, username, email)

                # 确保远程URL正确
                self.git.remote(path, clone_url)

                # 确保分支名正确（空仓库会先commit再rename）
                self.git.ensure_branch(path, target_branch)

                # 如果远程仓库有license，需要先pull合并
                if resp.status_code == 201 and lic:
                    self.git._run(["pull", "origin", target_branch, "--allow-unrelated-histories", "--no-edit"], cwd=path)
                    self.git.add_all(path)
                    self.git.commit(path, msg)
                elif resp.status_code == 201 and not lic:
                    # 已经在ensure_branch中commit过了，但可能有遗漏的文件
                    self.git.add_all(path)
                    ok_c, _, _ = self.git.commit(path, msg)
                    if not ok_c:
                        self.log("没有新的更改需要提交")

                ok, _, _ = self.git.push(path, "origin", target_branch)
                if ok:
                    self.log("上传完成！")
                    self._repos_cache.append({"path": path, "name": name, "url": html_url})
                    self.cfg["local_repos"] = self._repos_cache
                    save_config(self.cfg)
                else:
                    self.log("推送失败，尝试强制推送...")
                    ok2, _, _ = self.git.push(path, "origin", target_branch, force=True)
                    self.log("强制推送成功！" if ok2 else "推送失败，请检查网络和权限")
            except Exception as e:
                self.log(f"上传异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)

        threading.Thread(target=task, daemon=True).start()

    def _do_create_repo(self):
        if not self._need_auth():
            return
        name = self.up_name.get().strip()
        
        # 验证仓库名称
        is_valid, error_msg = validate_repo_name(name)
        if not is_valid:
            messagebox.showerror("输入错误", error_msg)
            return

        self._show_loading("正在创建远程仓库...")

        def task():
            try:
                lic = LICENSES.get(self.up_license.get(), "")
                self.log(f"正在创建远程仓库：{name}...")
                resp = self.api.create_repo(name, self.up_desc.get().strip(),
                                             self.up_priv.get(), lic, auto_init=True)
                if resp.status_code == 201:
                    self.log(f"仓库创建成功：{self.api.get_html_url(resp.json())}")
                elif resp.status_code == 422:
                    self.log(f"仓库 {name} 已存在")
                else:
                    self.log(f"创建失败：{resp.status_code} {resp.text}")
            except Exception as e:
                self.log(f"创建异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)

        threading.Thread(target=task, daemon=True).start()

    # ─────────────────── 更新 ───────────────────

    def _do_commit_push(self):
        path = self.ud_path.get().strip()
        if not path or not os.path.isdir(path):
            messagebox.showerror("错误", "请选择有效的本地项目路径")
            return
        
        # 验证分支名
        branch = self.ud_branch.get().strip() or "main"
        is_valid, error_msg = validate_branch_name(branch)
        if not is_valid:
            messagebox.showerror("输入错误", f"分支名无效：{error_msg}")
            return
        
        self._show_loading("正在提交并推送...")

        def task():
            try:
                msg = self.ud_msg.get().strip() or "Update"
                self.git.add_all(path)
                self.git.commit(path, msg)
                ok, _, _ = self.git.push(path, "origin", branch, force=self.ud_force.get())
                self.log("推送完成！" if ok else "推送失败")
            except Exception as e:
                self.log(f"操作异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _do_commit(self):
        path = self.ud_path.get().strip()
        if not path:
            return
        self._show_loading("正在提交...")
        def task():
            try:
                self.git.add_all(path)
                ok, _, _ = self.git.commit(path, self.ud_msg.get().strip() or "Update")
                self.log("提交完成" if ok else "没有更改需要提交")
            except Exception as e:
                self.log(f"提交异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _do_push(self):
        path = self.ud_path.get().strip()
        if not path:
            return
        
        # 验证分支名
        branch = self.ud_branch.get().strip() or "main"
        is_valid, error_msg = validate_branch_name(branch)
        if not is_valid:
            messagebox.showerror("输入错误", f"分支名无效：{error_msg}")
            return
        
        self._show_loading("正在推送...")
        def task():
            try:
                ok, _, _ = self.git.push(path, "origin", branch, self.ud_force.get())
                self.log("推送完成！" if ok else "推送失败")
            except Exception as e:
                self.log(f"推送异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _do_pull(self):
        path = self.ud_path.get().strip()
        if not path:
            return
        
        # 验证分支名
        branch = self.ud_branch.get().strip() or "main"
        is_valid, error_msg = validate_branch_name(branch)
        if not is_valid:
            messagebox.showerror("输入错误", f"分支名无效：{error_msg}")
            return
        
        self._show_loading("正在拉取远程代码...")
        def task():
            try:
                self.git.pull(path, "origin", branch)
            except Exception as e:
                self.log(f"拉取异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _refresh_status(self):
        path = self.ud_path.get().strip()
        if not path:
            return
        self.ud_status.delete("1.0", tk.END)
        s = self.git.status(path)
        self.ud_status.insert(tk.END, s if s else "工作区干净，无更改")
        br = self.git.current_branch(path)
        if br:
            self.ud_status.insert(tk.END, f"\n\n当前分支：{br}")
            self.ud_branch.set(br)
        lg = self.git.log(path, 5)
        if lg:
            self.ud_status.insert(tk.END, f"\n\n最近提交：\n{lg}")

    # ─────────────────── 分支 ───────────────────

    def _load_branches(self):
        if not self._need_auth():
            return
        rp = self.br_repo.get().strip()
        
        # 验证 owner/repo 格式
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            messagebox.showwarning("提示", error_msg)
            return
        
        self._show_loading("正在加载分支列表...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                branches = self.api.list_branches(owner, repo)
                self.br_list.delete(0, tk.END)
                for b in branches:
                    self.br_list.insert(tk.END, b["name"])
                self.log(f"加载了 {len(branches)} 个分支")
            except Exception as e:
                self.log(f"加载分支失败：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _br_local(self):
        path = self.br_path.get().strip()
        if not path:
            messagebox.showerror("错误", "请选择本地项目路径")
            return
        nb = self.br_new.get().strip()
        
        # 验证新分支名
        is_valid, error_msg = validate_branch_name(nb)
        if not is_valid:
            messagebox.showerror("输入错误", f"分支名无效：{error_msg}")
            return
        
        # 验证基础分支名
        base = self.br_base.get().strip() or "main"
        is_valid, error_msg = validate_branch_name(base)
        if not is_valid:
            messagebox.showerror("输入错误", f"基础分支名无效：{error_msg}")
            return
        
        self._show_loading("正在创建本地分支...")
        def task():
            try:
                self.git.checkout(path, base)
                ok, _, _ = self.git.checkout(path, nb, create=True)
                self.log(f"本地分支 {nb} 创建成功" if ok else "创建分支失败")
            except Exception as e:
                self.log(f"创建分支异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _br_remote(self):
        if not self._need_auth():
            return
        rp = self.br_repo.get().strip()
        
        # 验证 owner/repo 格式
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            messagebox.showerror("输入错误", error_msg)
            return
        
        nb = self.br_new.get().strip()
        
        # 验证新分支名
        is_valid, error_msg = validate_branch_name(nb)
        if not is_valid:
            messagebox.showerror("输入错误", f"分支名无效：{error_msg}")
            return
        
        # 验证基础分支名
        base = self.br_base.get().strip() or "main"
        is_valid, error_msg = validate_branch_name(base)
        if not is_valid:
            messagebox.showerror("输入错误", f"基础分支名无效：{error_msg}")
            return
        
        self._show_loading("正在创建远程分支...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                sha = self.api.get_branch_sha(owner, repo, base)
                if not sha:
                    self.log(f"无法获取基础分支 {base} 的SHA")
                    return
                resp = self.api.create_branch(owner, repo, nb, sha)
                if resp.status_code in (201, 200):
                    self.log(f"远程分支 {nb} 创建成功")
                    self.root.after(0, self._load_branches)
                else:
                    self.log(f"创建失败：{resp.status_code} {resp.text}")
            except Exception as e:
                self.log(f"创建远程分支异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _br_switch(self):
        path = self.br_path.get().strip()
        if not path:
            messagebox.showerror("错误", "请选择本地项目路径")
            return
        sel = self.br_list.curselection()
        if not sel:
            messagebox.showwarning("提示", "请先选择一个分支")
            return
        br = self.br_list.get(sel[0])
        
        # 确认切换
        if not self._confirm_dialog("确认切换", f"确定要切换到分支 {br} 吗？"):
            return
        
        self._show_loading(f"正在切换到分支 {br}...")
        def task():
            try:
                ok, _, _ = self.git.checkout(path, br)
                self.log(f"已切换到分支：{br}" if ok else "切换失败")
            except Exception as e:
                self.log(f"切换分支异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _br_delete(self):
        if not self._need_auth():
            return
        rp = self.br_repo.get().strip()
        
        # 验证 owner/repo 格式
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            return
        
        sel = self.br_list.curselection()
        if not sel:
            messagebox.showwarning("提示", "请先选择一个分支")
            return
        br = self.br_list.get(sel[0])
        
        # 确认删除
        if not self._confirm_dialog("确认删除", f"确定要删除远程分支 {br} 吗？\n\n此操作不可撤销！"):
            return
        
        self._show_loading(f"正在删除远程分支 {br}...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                resp = self.api.delete_branch(owner, repo, br)
                if resp.status_code in (204, 200):
                    self.log(f"远程分支 {br} 已删除")
                    self.root.after(0, self._load_branches)
                else:
                    self.log(f"删除失败：{resp.status_code} {resp.text}")
            except Exception as e:
                self.log(f"删除分支异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    # ─────────────────── Fork ───────────────────

    def _do_fork(self):
        if not self._need_auth():
            return
        rp = self.fk_repo.get().strip()
        
        # 验证 owner/repo 格式
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            messagebox.showerror("输入错误", error_msg)
            return
        
        self._show_loading("正在Fork仓库...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                self.log(f"正在Fork：{owner}/{repo}...")
                resp = self.api.fork_repo(owner, repo)
                if resp.status_code in (202, 201, 200):
                    fd = resp.json()
                    self.log(f"Fork成功：{self.api.get_html_url(fd)}")
                    if self.fk_auto.get():
                        lp = self.fk_local.get().strip() or os.path.join(os.getcwd(), repo)
                        self.git.clone(self.api.get_clone_url(fd), lp)
                        self.log(f"克隆完成：{lp}")
                else:
                    self.log(f"Fork失败：{resp.status_code} {resp.text}")
            except Exception as e:
                self.log(f"Fork异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _do_clone(self):
        url = self.fk_repo.get().strip()
        lp = self.fk_local.get().strip()
        if not url:
            messagebox.showerror("错误", "请输入仓库地址或 用户名/仓库名")
            return
        if not lp:
            messagebox.showerror("错误", "请选择克隆目标路径")
            return
        if "/" in url and not url.startswith("http"):
            url = f"{PLATFORMS[self.platform]['web']}/{url}.git"
        
        self._show_loading("正在克隆仓库...")
        def task():
            try:
                self.git.clone(url, lp)
            except Exception as e:
                self.log(f"克隆异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _fk_load(self):
        if not self._need_auth():
            return
        self._show_loading("正在加载仓库列表...")
        def task():
            try:
                repos = self.api.list_repos()
                self.fk_list.delete(0, tk.END)
                for r in repos:
                    vis = "Private" if r["private"] else "Public"
                    self.fk_list.insert(tk.END, f"{r['full_name']}  [{vis}]")
                self.log(f"加载了 {len(repos)} 个仓库")
            except Exception as e:
                self.log(f"加载仓库列表失败：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _fk_selected(self):
        sel = self.fk_list.curselection()
        if not sel:
            messagebox.showwarning("提示", "请先选择一个仓库")
            return
        text = self.fk_list.get(sel[0])
        self.fk_repo.set(text.split("  ")[0].strip())
        self._do_fork()

    # ─────────────────── 我的仓库 ───────────────────

    def _repos_load(self):
        if not self._need_auth():
            return
        self._show_loading("正在加载我的仓库列表...")
        def task():
            try:
                repos = self.api.list_repos()
                def update():
                    for i in self.repo_tree.get_children():
                        self.repo_tree.delete(i)
                    for r in repos:
                        vis = "私有" if r["private"] else "公开"
                        lang = r.get("language") or ""
                        lic = ""
                        if r.get("license"):
                            lic = r["license"].get("spdx_id", "") or r["license"].get("name", "") or ""
                        updated = (r.get("updated_at") or r.get("updated_at", ""))[:10]
                        self.repo_tree.insert("", tk.END, values=(r["full_name"], vis, lic, lang, updated))
                self.root.after(0, update)
                self.log(f"加载了 {len(repos)} 个仓库")
            except Exception as e:
                self.log(f"加载仓库列表失败：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _repos_open(self):
        sel = self.repo_tree.selection()
        if not sel:
            return
        name = self.repo_tree.item(sel[0], "values")[0]
        webbrowser.open(f"{PLATFORMS[self.platform]['web']}/{name}")

    # ─────────────────── 辅助 ───────────────────

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        def _():
            self.log_box.insert(tk.END, f"[{ts}] {msg}\n")
            self.log_box.see(tk.END)
        if threading.current_thread() is threading.main_thread():
            _()
        else:
            self.root.after(0, _)

    def _refresh(self):
        token = self.cfg.get(f"token_{self.platform}", self.cfg.get("token", ""))
        if token:
            self._set_token(token)

    def run(self):
        atexit.register(self._cleanup)
        self.root.mainloop()


if __name__ == "__main__":
    App().run()

