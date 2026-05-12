#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub/Gitee Manager v10.1 - 本地代码托管管理工具
Author: LZF
Version: 10.1.0
"""

__author__ = "LZF"
__version__ = "10.1.0"

import os
import sys
import json
import subprocess
import threading
import atexit
import time
import csv
import io
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, colorchooser, simpledialog
import webbrowser
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

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
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".code_manager")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
PROFILES_DIR = os.path.join(CONFIG_DIR, "profiles")
LOGS_DIR = os.path.join(CONFIG_DIR, "logs")
HISTORY_FILE = os.path.join(CONFIG_DIR, "history.json")
ICON_PATH = os.path.join(_BUNDLE_DIR, "icon.png")
WEIXIN_PATH = os.path.join(_BUNDLE_DIR, "weixin.png")
GIT_DOWNLOAD_URL = "https://git-scm.com/download/win"

os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(PROFILES_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

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

# ──────────────────────────── .gitignore 模板 ────────────────────────────

GITIGNORE_TEMPLATES = {
    "Python": """# Python
*.pyc
__pycache__/
*.egg-info/
dist/
build/
.env
venv/
.venv/
*.egg
.pytest_cache/
.mypy_cache/
""",
    "Node.js": """# Node.js
node_modules/
npm-debug.log
yarn-error.log
.env
dist/
build/
.DS_Store
""",
    "Java": """# Java
*.class
*.jar
*.war
target/
.gradle/
.idea/
*.iml
""",
    "C/C++": """# C/C++
*.o
*.obj
*.exe
*.dll
*.so
*.dylib
build/
.vs/
*.suo
*.user
""",
    "Go": """# Go
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
vendor/
""",
    "通用": """# 通用
.DS_Store
Thumbs.db
*.log
*.tmp
*.bak
*.swp
*~
.idea/
.vscode/
.project
.settings/
.classpath
"""
}

# ──────────────────────────── 预设主题 ────────────────────────────

THEMES = {
    "Modern": {
        "light": {
            "bg": "#fafafa", "bg2": "#ffffff", "bg3": "#f5f5f5",
            "fg": "#171717", "fg2": "#666666", "fg3": "#a3a3a3",
            "accent": "#2563eb", "accent_hover": "#1d4ed8",
            "accent_gradient": ("#2563eb", "#7c3aed"),
            "header_bg": "#ffffff", "header_fg": "#171717",
            "btn_bg": "#2563eb", "btn_fg": "#ffffff",
            "btn2_bg": "#f5f5f5", "btn2_fg": "#171717",
            "entry_bg": "#ffffff", "entry_fg": "#171717",
            "select_bg": "#dbeafe", "select_fg": "#171717",
            "log_bg": "#f8fafc", "log_fg": "#171717",
            "tree_bg": "#ffffff", "tree_fg": "#171717",
            "tree_heading_bg": "#f1f5f9",
            "border": "#e5e7eb",
            "tab_bg": "#ffffff", "tab_active": "#ffffff",
            "sidebar_bg": "#f1f5f9", "sidebar_fg": "#64748b", "sidebar_active": "#2563eb",
            "card_bg": "#ffffff", "card_border": "#e2e8f0",
            "tooltip_bg": "#1e293b", "tooltip_fg": "#f8fafc",
        },
        "dark": {
            "bg": "#0a0a0a", "bg2": "#171717", "bg3": "#1a1a1a",
            "fg": "#fafafa", "fg2": "#a3a3a3", "fg3": "#525252",
            "accent": "#3b82f6", "accent_hover": "#60a5fa",
            "accent_gradient": ("#3b82f6", "#8b5cf6"),
            "header_bg": "#0a0a0a", "header_fg": "#fafafa",
            "btn_bg": "#3b82f6", "btn_fg": "#ffffff",
            "btn2_bg": "#262626", "btn2_fg": "#fafafa",
            "entry_bg": "#171717", "entry_fg": "#fafafa",
            "select_bg": "#1e3a5f", "select_fg": "#fafafa",
            "log_bg": "#0a0a0a", "log_fg": "#a3a3a3",
            "tree_bg": "#171717", "tree_fg": "#fafafa",
            "tree_heading_bg": "#262626",
            "border": "#262626",
            "tab_bg": "#171717", "tab_active": "#0a0a0a",
            "sidebar_bg": "#111111", "sidebar_fg": "#737373", "sidebar_active": "#3b82f6",
            "card_bg": "#171717", "card_border": "#262626",
            "tooltip_bg": "#e2e8f0", "tooltip_fg": "#0a0a0a",
        }
    },
    "微信(默认)": {
        "light": {
            "bg": "#f8f9fa", "bg2": "#ffffff", "bg3": "#f0f1f3",
            "fg": "#1a1a2e", "fg2": "#4a4a6a", "fg3": "#8a8aa0",
            "accent": "#07c160", "accent_hover": "#06ad56",
            "header_bg": "#1a1a2e", "header_fg": "#ffffff",
            "btn_bg": "#07c160", "btn_fg": "#ffffff",
            "btn2_bg": "#f0f1f3", "btn2_fg": "#1a1a2e",
            "entry_bg": "#ffffff", "entry_fg": "#1a1a2e",
            "select_bg": "#d4edda", "select_fg": "#1a1a2e",
            "log_bg": "#fafbfc", "log_fg": "#1a1a2e",
            "tree_bg": "#ffffff", "tree_fg": "#1a1a2e",
            "tree_heading_bg": "#f0f1f3",
            "border": "#e2e4e8",
            "tab_bg": "#f0f1f3", "tab_active": "#ffffff",
        },
        "dark": {
            "bg": "#0d1117", "bg2": "#161b22", "bg3": "#1c2128",
            "fg": "#e6edf3", "fg2": "#8b949e", "fg3": "#6e7681",
            "accent": "#07c160", "accent_hover": "#06ad56",
            "header_bg": "#010409", "header_fg": "#e6edf3",
            "btn_bg": "#07c160", "btn_fg": "#ffffff",
            "btn2_bg": "#21262d", "btn2_fg": "#e6edf3",
            "entry_bg": "#0d1117", "entry_fg": "#e6edf3",
            "select_bg": "#0a4a2a", "select_fg": "#e6edf3",
            "log_bg": "#0d1117", "log_fg": "#8b949e",
            "tree_bg": "#0d1117", "tree_fg": "#e6edf3",
            "tree_heading_bg": "#161b22",
            "border": "#30363d",
            "tab_bg": "#161b22", "tab_active": "#0d1117",
        }
    },
    "VSCode": {
        "light": {
            "bg": "#f8f9fa", "bg2": "#ffffff", "bg3": "#f0f1f3",
            "fg": "#1a1a2e", "fg2": "#4a4a6a", "fg3": "#8a8aa0",
            "accent": "#007acc", "accent_hover": "#0062a3",
            "header_bg": "#1e1e1e", "header_fg": "#ffffff",
            "btn_bg": "#007acc", "btn_fg": "#ffffff",
            "btn2_bg": "#f0f1f3", "btn2_fg": "#1a1a2e",
            "entry_bg": "#ffffff", "entry_fg": "#1a1a2e",
            "select_bg": "#cce8ff", "select_fg": "#1a1a2e",
            "log_bg": "#fafbfc", "log_fg": "#1a1a2e",
            "tree_bg": "#ffffff", "tree_fg": "#1a1a2e",
            "tree_heading_bg": "#f0f1f3",
            "border": "#e2e4e8",
            "tab_bg": "#f0f1f3", "tab_active": "#ffffff",
        },
        "dark": {
            "bg": "#0d1117", "bg2": "#161b22", "bg3": "#1c2128",
            "fg": "#e6edf3", "fg2": "#8b949e", "fg3": "#6e7681",
            "accent": "#007acc", "accent_hover": "#1a8ad4",
            "header_bg": "#010409", "header_fg": "#e6edf3",
            "btn_bg": "#0e639c", "btn_fg": "#ffffff",
            "btn2_bg": "#21262d", "btn2_fg": "#e6edf3",
            "entry_bg": "#0d1117", "entry_fg": "#e6edf3",
            "select_bg": "#094771", "select_fg": "#e6edf3",
            "log_bg": "#0d1117", "log_fg": "#8b949e",
            "tree_bg": "#0d1117", "tree_fg": "#e6edf3",
            "tree_heading_bg": "#161b22",
            "border": "#30363d",
            "tab_bg": "#161b22", "tab_active": "#0d1117",
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
        "sidebar_bg": "#f0f0f0", "sidebar_fg": "#666666", "sidebar_active": "#4a90d9",
        "card_bg": "#ffffff", "card_border": "#e0e0e0",
        "tooltip_bg": "#333333", "tooltip_fg": "#ffffff",
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
        "sidebar_bg": "#252525", "sidebar_fg": "#888888", "sidebar_active": "#4a90d9",
        "card_bg": "#2d2d2d", "card_border": "#404040",
        "tooltip_bg": "#e0e0e0", "tooltip_fg": "#333333",
    }
}

# ──────────────────────────── 工具函数 ────────────────────────────

def load_config(profile="default"):
    config_file = os.path.join(PROFILES_DIR, f"{profile}.json")
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    elif os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    else:
        cfg = {}
    
    # 环境变量覆盖
    if os.environ.get("CM_TOKEN_GITHUB"):
        cfg["token_github"] = os.environ["CM_TOKEN_GITHUB"]
    if os.environ.get("CM_TOKEN_GITEE"):
        cfg["token_gitee"] = os.environ["CM_TOKEN_GITEE"]
    if os.environ.get("CM_PROXY"):
        cfg["proxy"] = os.environ["CM_PROXY"]
    
    return cfg

def save_config(config, profile="default"):
    config_file = os.path.join(PROFILES_DIR, f"{profile}.json")
    with open(config_file, "w", encoding="utf-8") as f:
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
    import re
    if not name:
        return False, "仓库名称不能为空"
    if not re.match(r'^[a-zA-Z0-9._-]+$', name):
        return False, "仓库名称只能包含字母、数字、点、下划线和连字符"
    if len(name) > 100:
        return False, "仓库名称不能超过100个字符"
    return True, ""

def validate_branch_name(name):
    import re
    if not name:
        return False, "分支名不能为空"
    if not re.match(r'^[a-zA-Z0-9._/-]+$', name):
        return False, "分支名只能包含字母、数字、点、下划线、连字符和斜杠"
    if '..' in name or name.startswith('.') or name.endswith('.'):
        return False, "分支名不能包含连续的点，也不能以点开头或结尾"
    return True, ""

def validate_owner_repo(text):
    if not text or '/' not in text:
        return False, "请输入格式：用户名/仓库名"
    parts = text.split('/', 1)
    if not parts[0] or not parts[1]:
        return False, "用户名和仓库名都不能为空"
    return True, ""


# ──────────────────────────── ToolTip 类 ────────────────────────────

class ToolTip:
    """自定义美化提示框"""
    def __init__(self, widget, text, theme=None, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self._tip_window = None
        self._after_id = None
        t = theme or {}
        self._bg = t.get("tooltip_bg", "#1e293b")
        self._fg = t.get("tooltip_fg", "#f8fafc")
        self._font = t.get("tooltip_font", ("Segoe UI", 9))
        widget.bind("<Enter>", self._on_enter, add="+")
        widget.bind("<Leave>", self._on_leave, add="+")
        widget.bind("<ButtonPress>", self._on_leave, add="+")

    def _on_enter(self, event=None):
        self._cancel()
        self._after_id = self.widget.after(self.delay, self._show)

    def _on_leave(self, event=None):
        self._cancel()
        self._hide()

    def _cancel(self):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None

    def _show(self):
        if self._tip_window:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self._tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        try:
            tw.wm_attributes("-topmost", True)
        except Exception:
            pass
        frame = tk.Frame(tw, bg=self._bg, highlightbackground=self._bg,
                         highlightthickness=1, padx=8, pady=4)
        frame.pack()
        lbl = tk.Label(frame, text=self.text, bg=self._bg, fg=self._fg,
                       font=self._font, anchor=tk.W, justify=tk.LEFT)
        lbl.pack()

    def _hide(self):
        if self._tip_window:
            self._tip_window.destroy()
            self._tip_window = None

    def update_text(self, text):
        self.text = text

    def destroy(self):
        self._cancel()
        self._hide()


# ──────────────────────────── GradientButton 类 ────────────────────────────

class GradientButton(tk.Canvas):
    """渐变色圆角按钮"""
    def __init__(self, parent, text, command=None,
                 gradient_colors=("#2563eb", "#7c3aed"),
                 fg="#ffffff", width=160, height=36,
                 font=("Segoe UI", 10, "bold"), **kwargs):
        super().__init__(parent, width=width, height=height,
                         highlightthickness=0, bg=parent.cget("bg") if isinstance(parent, tk.Frame) else "#ffffff", **kwargs)
        self._width = width
        self._height = height
        self._text = text
        self._command = command
        self._colors = gradient_colors
        self._fg = fg
        self._font = font
        self._hover = False
        self._draw(gradient_colors)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.configure(cursor="hand2")

    def _lerp_color(self, c1, c2, t):
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _brighten(self, color, amount=0.15):
        white = "#ffffff"
        return self._lerp_color(color, white, amount)

    def _draw(self, colors):
        self.delete("all")
        w, h = self._width, self._height
        r = 6
        steps = w
        for i in range(steps):
            ratio = i / max(steps - 1, 1)
            c = self._lerp_color(colors[0], colors[1], ratio)
            x0 = i
            self.create_line(x0, 0, x0, h, fill=c)
        self.create_arc(0, 0, 2*r, 2*r, start=90, extent=90, fill=colors[0], outline="")
        self.create_arc(w-2*r, 0, w, 2*r, start=0, extent=90, fill=colors[1], outline="")
        self.create_arc(0, h-2*r, 2*r, h, start=180, extent=90, fill=colors[0], outline="")
        self.create_arc(w-2*r, h-2*r, w, h, start=270, extent=90, fill=colors[1], outline="")
        self.create_rectangle(r, 0, w-r, h, fill=colors[0], outline="")
        self.create_rectangle(0, r, w, h-r, fill=colors[0], outline="")
        for i in range(steps):
            ratio = i / max(steps - 1, 1)
            c = self._lerp_color(colors[0], colors[1], ratio)
            x0 = i
            self.create_line(x0, 1, x0, h-1, fill=c)
        self.create_text(w//2, h//2, text=self._text, fill=self._fg, font=self._font)

    def _on_enter(self, event=None):
        self._hover = True
        bright = (self._brighten(self._colors[0]), self._brighten(self._colors[1]))
        self._draw(bright)

    def _on_leave(self, event=None):
        self._hover = False
        self._draw(self._colors)

    def _on_click(self, event=None):
        if self._command:
            self._command()

    def set_colors(self, colors):
        self._colors = colors
        self._draw(colors)

    def set_text(self, text):
        self._text = text
        self._draw(self._colors)

    def set_command(self, command):
        self._command = command


# ──────────────────────────── Logger 类 ────────────────────────────

class Logger:
    def __init__(self, log_dir=None, ui_callback=None):
        self.log_dir = log_dir or LOGS_DIR
        os.makedirs(self.log_dir, exist_ok=True)
        self.ui_callback = ui_callback
        self.history_file = HISTORY_FILE
        self._max_size = 5 * 1024 * 1024  # 5MB
        self._max_files = 5

    def log(self, msg, level="INFO"):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] [{level}] {msg}"
        self._write_to_file(line)
        if self.ui_callback:
            self.ui_callback(f"[{datetime.now():%H:%M:%S}] {msg}")

    def add_history(self, action, detail, platform="", repo=""):
        history = self._load_history()
        history.append({
            "time": datetime.now().isoformat(),
            "action": action,
            "detail": detail,
            "platform": platform,
            "repo": repo
        })
        if len(history) > 1000:
            history = history[-1000:]
        self._save_history(history)

    def get_history(self, limit=50):
        history = self._load_history()
        return history[-limit:]

    def clear_history(self):
        self._save_history([])

    def _write_to_file(self, line):
        log_file = os.path.join(self.log_dir, f"{datetime.now():%Y-%m-%d}.log")
        if os.path.exists(log_file) and os.path.getsize(log_file) > self._max_size:
            self._rotate_logs(log_file)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def _rotate_logs(self, log_file):
        for i in range(self._max_files - 1, 0, -1):
            src = f"{log_file}.{i}" if i > 1 else log_file
            dst = f"{log_file}.{i + 1}"
            if os.path.exists(src):
                if i == self._max_files - 1:
                    os.remove(src)
                else:
                    os.rename(src, dst)

    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return []

    def _save_history(self, history):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

# ──────────────────────────── NetworkManager 类 ────────────────────────────

class NetworkManager:
    def __init__(self, logger=None, proxy=None, timeout=30):
        self.logger = logger
        self.proxy = proxy
        self.timeout = timeout
        self._session = requests.Session()
        if proxy:
            self._session.proxies = {"http": proxy, "https": proxy}

    def request(self, method, url, headers=None, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        if headers:
            kwargs["headers"] = headers

        for attempt in range(3):
            try:
                r = self._session.request(method, url, **kwargs)
                if r.status_code == 429:
                    wait = int(r.headers.get("Retry-After", 60))
                    if self.logger:
                        self.logger.log(f"API限流，等待{wait}秒...", "WARNING")
                    time.sleep(wait)
                    continue
                return r
            except requests.exceptions.Timeout:
                if attempt < 2:
                    wait = 2 ** attempt
                    if self.logger:
                        self.logger.log(f"请求超时，{wait}秒后重试...", "WARNING")
                    time.sleep(wait)
                    continue
                raise
            except requests.exceptions.ConnectionError:
                if attempt < 2:
                    wait = 2 ** attempt
                    if self.logger:
                        self.logger.log(f"连接失败，{wait}秒后重试...", "WARNING")
                    time.sleep(wait)
                    continue
                raise

    def set_proxy(self, proxy):
        self.proxy = proxy
        self._session.proxies = {"http": proxy, "https": proxy} if proxy else {}

    def set_timeout(self, timeout):
        self.timeout = timeout

# ──────────────────────────── ConfigManager 类 ────────────────────────────

class ConfigManager:
    def __init__(self, config_dir=None):
        self.config_dir = config_dir or CONFIG_DIR
        self.profiles_dir = os.path.join(self.config_dir, "profiles")
        os.makedirs(self.profiles_dir, exist_ok=True)

    def load_profile(self, name="default"):
        return load_config(name)

    def save_profile(self, name, config):
        save_config(config, name)

    def list_profiles(self):
        profiles = []
        if os.path.exists(self.profiles_dir):
            for f in os.listdir(self.profiles_dir):
                if f.endswith(".json"):
                    profiles.append(f[:-5])
        return profiles if profiles else ["default"]

    def delete_profile(self, name):
        if name == "default":
            return False
        profile_file = os.path.join(self.profiles_dir, f"{name}.json")
        if os.path.exists(profile_file):
            os.remove(profile_file)
            return True
        return False

    def export_config(self, path, profile="default"):
        config = self.load_profile(profile)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True

    def import_config(self, path, profile="default"):
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
        self.save_profile(profile, config)
        return True

# ──────────────────────────── 平台 API ────────────────────────────

class PlatformAPI:
    def __init__(self, platform, token, logger=None, proxy=None, timeout=30):
        self.platform = platform
        self.base = PLATFORMS[platform]["api"]
        self.web = PLATFORMS[platform]["web"]
        self.is_github = (platform == "GitHub")
        self.logger = logger
        self._token = token

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

        self._net = NetworkManager(logger=logger, proxy=proxy, timeout=timeout)

    def _req(self, method, url, **kwargs):
        kwargs["headers"] = self.headers
        return self._net.request(method, url, **kwargs)

    # ─── 用户相关 ───

    def get_user(self):
        r = self._req("GET", f"{self.base}/user")
        if r.status_code == 200:
            d = r.json()
            if self.is_github:
                return d
            return {"login": d.get("login") or d.get("name", ""), "email": d.get("email", "N/A")}
        return None

    # ─── 仓库相关 ───

    def list_repos(self, page=1, per_page=100):
        repos = []
        while True:
            params = {"per_page": per_page, "page": page, "sort": "updated"}
            if not self.is_github:
                params["type"] = "all"
            r = self._req("GET", f"{self.base}/user/repos", params=params)
            if r.status_code != 200 or not r.json():
                break
            repos.extend(r.json())
            page += 1
            if len(r.json()) < per_page:
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

    def delete_repo(self, owner, repo):
        return self._req("DELETE", f"{self.base}/repos/{owner}/{repo}")

    def fork_repo(self, owner, repo):
        return self._req("POST", f"{self.base}/repos/{owner}/{repo}/forks")

    def search_repos(self, query, page=1, per_page=20):
        if self.is_github:
            url = f"{self.base}/search/repositories"
            params = {"q": query, "per_page": per_page, "page": page}
        else:
            url = f"{self.base}/projects/search"
            params = {"q": query, "per_page": per_page, "page": page}
        r = self._req("GET", url, params=params)
        if r.status_code == 200:
            data = r.json()
            return data.get("items", data.get("projects", []))
        return []

    # ─── 分支相关 ───

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

    # ─── Release相关 ───

    def list_releases(self, owner, repo):
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
        return None

    # ─── Issue管理 ───

    def list_issues(self, owner, repo, state="open", page=1, per_page=30):
        params = {"state": state, "per_page": per_page, "page": page}
        r = self._req("GET", f"{self.base}/repos/{owner}/{repo}/issues", params=params)
        return r.json() if r.status_code == 200 else []

    def create_issue(self, owner, repo, title, body="", labels=None, assignees=None):
        data = {"title": title, "body": body}
        if labels:
            data["labels"] = labels
        if assignees:
            data["assignees"] = assignees
        return self._req("POST", f"{self.base}/repos/{owner}/{repo}/issues", json=data)

    def update_issue(self, owner, repo, issue_number, title=None, body=None, state=None):
        data = {}
        if title:
            data["title"] = title
        if body:
            data["body"] = body
        if state:
            data["state"] = state
        return self._req("PATCH", f"{self.base}/repos/{owner}/{repo}/issues/{issue_number}", json=data)

    def close_issue(self, owner, repo, issue_number):
        return self.update_issue(owner, repo, issue_number, state="closed")

    # ─── PR管理 ───

    def list_pulls(self, owner, repo, state="open", page=1, per_page=30):
        params = {"state": state, "per_page": per_page, "page": page}
        r = self._req("GET", f"{self.base}/repos/{owner}/{repo}/pulls", params=params)
        return r.json() if r.status_code == 200 else []

    def create_pull(self, owner, repo, title, head, base="main", body=""):
        data = {"title": title, "head": head, "base": base, "body": body}
        return self._req("POST", f"{self.base}/repos/{owner}/{repo}/pulls", json=data)

    def merge_pull(self, owner, repo, pull_number, commit_message=""):
        data = {"commit_message": commit_message}
        return self._req("PUT", f"{self.base}/repos/{owner}/{repo}/pulls/{pull_number}/merge", json=data)

    def close_pull(self, owner, repo, pull_number):
        data = {"state": "closed"}
        return self._req("PATCH", f"{self.base}/repos/{owner}/{repo}/pulls/{pull_number}", json=data)

    # ─── Webhook管理 ───

    def list_webhooks(self, owner, repo):
        r = self._req("GET", f"{self.base}/repos/{owner}/{repo}/hooks")
        return r.json() if r.status_code == 200 else []

    def create_webhook(self, owner, repo, url, events=None, secret=""):
        if events is None:
            events = ["push"]
        data = {
            "name": "web",
            "active": True,
            "events": events,
            "config": {
                "url": url,
                "content_type": "json",
                "secret": secret
            }
        }
        return self._req("POST", f"{self.base}/repos/{owner}/{repo}/hooks", json=data)

    def delete_webhook(self, owner, repo, hook_id):
        return self._req("DELETE", f"{self.base}/repos/{owner}/{repo}/hooks/{hook_id}")

    def test_webhook(self, owner, repo, hook_id):
        return self._req("POST", f"{self.base}/repos/{owner}/{repo}/hooks/{hook_id}/tests")

    # ─── 辅助方法 ───

    def get_clone_url(self, repo_data):
        if self.is_github:
            return repo_data.get("clone_url", "")
        url = repo_data.get("clone_url", "") or repo_data.get("html_url", "")
        return url if url.endswith(".git") else url.rstrip("/") + ".git"

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

    # ─── 新增功能 ───

    def create_gitignore(self, path, template="通用"):
        content = GITIGNORE_TEMPLATES.get(template, "")
        gitignore_path = os.path.join(path, ".gitignore")
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write(content)
        self.log_fn(f"已创建 .gitignore（模板：{template}）")
        return True

    def check_ssh(self):
        ssh_dir = os.path.expanduser("~/.ssh")
        if os.path.exists(ssh_dir):
            for key in ["id_rsa.pub", "id_ed25519.pub"]:
                if os.path.exists(os.path.join(ssh_dir, key)):
                    return True
        return False

    def pull_with_conflict_check(self, path, remote="origin", branch="main"):
        ok, out, err = self._run(["pull", remote, branch], cwd=path)
        output = (out or "") + (err or "")
        if not ok and "CONFLICT" in output:
            return False, "检测到冲突，请手动解决"
        return ok, output

    def get_submodules(self, path):
        ok, out, _ = self._run(["submodule", "status"], cwd=path)
        if ok and out.strip():
            return out.strip().split("\n")
        return []

# ──────────────────────────── 主应用 ────────────────────────────

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("1280x860")
        self.root.minsize(1100, 750)

        self.cfg = load_config()
        self.config_mgr = ConfigManager()
        self.current_profile = self.cfg.get("current_profile", "default")

        self.api = None
        self.user = None
        self.logger = Logger(ui_callback=None)  # UI回调在_build_ui后设置
        self.git = GitOps(log_fn=self._log_to_ui)
        self._repos_cache = self.cfg.get("local_repos", [])

        self.platform = self.cfg.get("platform", "GitHub")
        self.theme_name = self.cfg.get("theme", "微信(默认)")
        self.dark_mode = self.cfg.get("dark_mode", False)
        self.font_size = self.cfg.get("font_size", 9)
        self.custom_colors = self.cfg.get("custom_colors", CUSTOM_THEME_TEMPLATE.copy())
        self.proxy = self.cfg.get("proxy", "")
        self.timeout = self.cfg.get("timeout", 30)

        self._icon_img = None
        self._weixin_img = None
        self._icon_small = None
        self._weixin_small = None
        self._load_images()
        self._apply_theme()
        self._build_ui()

        # 设置Logger的UI回调
        self.logger.ui_callback = self._log_to_ui

        self._auto_login()
        self._check_git()

    def _log_to_ui(self, msg):
        """线程安全的日志写入UI"""
        def _():
            self.log_box.insert(tk.END, f"{msg}\n")
            self.log_box.see(tk.END)
        if threading.current_thread() is threading.main_thread():
            _()
        else:
            self.root.after(0, _)

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

        s.configure(".", background=t["bg"], foreground=t["fg"], font=("Segoe UI", fs))
        s.configure("TFrame", background=t["bg"])
        s.configure("TLabel", background=t["bg"], foreground=t["fg"], font=("Segoe UI", fs))
        s.configure("TButton", background=t["btn2_bg"], foreground=t["btn2_fg"],
                     font=("Segoe UI", fs), padding=(12, 6), relief="flat")
        s.map("TButton",
               background=[("active", t["accent"]), ("pressed", t["accent_hover"])],
               foreground=[("active", t["btn_fg"]), ("pressed", t["btn_fg"])])

        s.configure("Accent.TButton", background=t["btn_bg"], foreground=t["btn_fg"],
                     font=("Segoe UI", fsb, "bold"), padding=(16, 8), relief="flat")
        s.map("Accent.TButton",
               background=[("active", t["accent_hover"]), ("pressed", t["accent"])],
               foreground=[("active", t["btn_fg"])])

        s.configure("Header.TFrame", background=t["header_bg"], padding=8)
        s.configure("Header.TLabel", background=t["header_bg"], foreground=t["header_fg"],
                     font=("Segoe UI Semibold", fsh, "bold"))
        s.configure("Settings.TFrame", background=t["header_bg"])
        s.configure("Settings.TLabel", background=t["header_bg"], foreground=t["header_fg"],
                     font=("Segoe UI", fs))
        s.configure("Theme.TButton", background=t["header_bg"], foreground=t["header_fg"],
                     font=("Segoe UI", fs), padding=(8, 4), relief="flat")
        s.map("Theme.TButton",
               background=[("active", t["accent"])],
               foreground=[("active", "#ffffff")])

        s.configure("TNotebook", background=t["bg"], padding=4)
        s.configure("TNotebook.Tab", background=t["tab_bg"], foreground=t["fg2"],
                     padding=(20, 8), font=("Segoe UI", fs), relief="flat")
        s.map("TNotebook.Tab",
               background=[("selected", t["tab_active"])],
               foreground=[("selected", t["fg"])])

        s.configure("TEntry", fieldbackground=t["entry_bg"], foreground=t["entry_fg"],
                     insertcolor=t["entry_fg"], font=("Segoe UI", fs), relief="flat", padding=6)
        s.configure("TCombobox", fieldbackground=t["entry_bg"], foreground=t["entry_fg"],
                     font=("Segoe UI", fs), relief="flat", padding=6)

        s.configure("TLabelframe", background=t["bg"], foreground=t["fg"],
                     font=("Segoe UI", fsb), relief="flat", padding=8)
        s.configure("TLabelframe.Label", background=t["bg"], foreground=t["accent"],
                     font=("Segoe UI Semibold", fsb, "bold"))

        s.configure("Treeview", background=t["tree_bg"], foreground=t["tree_fg"],
                     fieldbackground=t["tree_bg"], font=("Segoe UI", fs), relief="flat", rowheight=28)
        s.configure("Treeview.Heading", background=t["tree_heading_bg"], foreground=t["fg2"],
                     font=("Segoe UI Semibold", fsb), relief="flat", padding=6)
        s.map("Treeview",
               background=[("selected", t["select_bg"])],
               foreground=[("selected", t["select_fg"])])

        s.configure("TSeparator", background=t["border"])
        s.configure("TRadiobutton", background=t["bg"], foreground=t["fg"], font=("Segoe UI", fs), padding=4)
        s.configure("TCheckbutton", background=t["bg"], foreground=t["fg"], font=("Segoe UI", fs), padding=4)
        s.configure("TScrollbar", background=t["bg3"], troughcolor=t["bg2"], arrowcolor=t["fg2"])

    def _rebuild_theme(self):
        self._apply_theme()
        t = self._current_theme
        self.root.configure(bg=t["bg"])
        for widget in self.root.winfo_children():
            widget.destroy()
        self._build_ui()
        self._show_tab(self._current_tab or "upload")


    def _update_status_bar(self):
        if hasattr(self, 'status_lbl'):
            self.status_lbl.config(text=f"v{APP_VERSION} | Author: {APP_AUTHOR} | 当前平台: {self.platform}")

    def _show_loading(self, message="处理中..."):
        self.log(message)
        self.root.config(cursor="wait")
        self.root.update()

    def _hide_loading(self):
        self.root.config(cursor="")

    def _confirm_dialog(self, title, message):
        return messagebox.askyesno(title, message, icon="warning")

    # ─────────────────── SIDEBAR_ITEMS ───────────────────
    SIDEBAR_ITEMS = [
        ("\U0001F4E4", "上传代码", "upload"),
        ("\U0001F504", "更新推送", "update"),
        ("\U0001F33F", "分支管理", "branch"),
        ("\U0001F374", "Fork仓库", "fork"),
        ("\U0001F4E6", "Release", "release"),
        ("\U0001F4C1", "我的仓库", "repos"),
        ("\U0001F50D", "搜索", "search"),
        ("\U0001F4AC", "Issue", "issues"),
        ("\U0001F500", "PR", "pulls"),
        ("\U0001FA9D", "Webhook", "webhook"),
        ("\U0001F4CA", "统计", "stats"),
        ("\u2699\uFE0F", "设置", "settings"),
        ("\u2139\uFE0F", "关于", "about"),
    ]

    def _build_ui(self):
        t = self._current_theme
        self.root.configure(bg=t["bg"])

        if self._icon_img:
            try:
                self.root.iconphoto(True, self._icon_img)
            except Exception:
                pass

        # 顶部栏
        hdr_bg = t.get("header_bg", t["bg2"])
        hdr = tk.Frame(self.root, bg=hdr_bg,
                       highlightbackground=t["border"], highlightthickness=1)
        hdr.pack(fill=tk.X, side=tk.TOP)

        self.user_lbl = tk.Label(hdr, text="未登录", bg=hdr_bg,
                                 fg=t["fg"], font=("Segoe UI", self.font_size))
        self.user_lbl.pack(side=tk.LEFT, padx=12, pady=6)

        ctrl = tk.Frame(hdr, bg=hdr_bg)
        ctrl.pack(side=tk.RIGHT, padx=12, pady=6)

        tk.Label(ctrl, text="平台:", bg=hdr_bg,
                 fg=t["fg2"], font=("Segoe UI", self.font_size)).pack(side=tk.LEFT, padx=(0, 2))
        self.platform_var = tk.StringVar(value=self.platform)
        plat_cb = ttk.Combobox(ctrl, textvariable=self.platform_var,
                               values=list(PLATFORMS.keys()), state="readonly", width=7)
        plat_cb.pack(side=tk.LEFT, padx=2)
        plat_cb.bind("<<ComboboxSelected>>", self._on_platform_change)

        tk.Label(ctrl, text="主题:", bg=hdr_bg,
                 fg=t["fg2"], font=("Segoe UI", self.font_size)).pack(side=tk.LEFT, padx=(8, 2))
        self.theme_var = tk.StringVar(value=self.theme_name)
        theme_cb = ttk.Combobox(ctrl, textvariable=self.theme_var,
                                values=list(THEMES.keys()) + ["自定义"], state="readonly", width=10)
        theme_cb.pack(side=tk.LEFT, padx=2)
        theme_cb.bind("<<ComboboxSelected>>", self._on_theme_change)

        tk.Label(ctrl, text="字号:", bg=hdr_bg,
                 fg=t["fg2"], font=("Segoe UI", self.font_size)).pack(side=tk.LEFT, padx=(8, 2))
        self.font_var = tk.StringVar(value=str(self.font_size))
        font_cb = ttk.Combobox(ctrl, textvariable=self.font_var,
                               values=["8", "9", "10", "11", "12", "13", "14"],
                               state="readonly", width=3)
        font_cb.pack(side=tk.LEFT, padx=2)
        font_cb.bind("<<ComboboxSelected>>", self._on_font_change)

        tk.Label(ctrl, text="深色:", bg=hdr_bg,
                 fg=t["fg2"], font=("Segoe UI", self.font_size)).pack(side=tk.LEFT, padx=(8, 2))
        self.dark_var = tk.BooleanVar(value=self.dark_mode)
        ttk.Checkbutton(ctrl, variable=self.dark_var, command=self._on_dark_toggle).pack(side=tk.LEFT, padx=2)

        sep = tk.Frame(ctrl, width=1, height=20, bg=t["border"])
        sep.pack(side=tk.LEFT, padx=8, fill=tk.Y)
        ttk.Button(ctrl, text="Token设置", command=self._token_dlg, style="Theme.TButton").pack(side=tk.LEFT, padx=2)
        ttk.Button(ctrl, text="刷新", command=self._refresh, style="Theme.TButton").pack(side=tk.LEFT, padx=2)

        # 主体: 侧边栏 + 内容区
        body = tk.Frame(self.root, bg=t["bg"])
        body.pack(fill=tk.BOTH, expand=True)

        # 侧边栏
        sidebar_bg = t.get("sidebar_bg", t["bg3"])
        self.sidebar = tk.Frame(body, bg=sidebar_bg,
                                width=200, highlightbackground=t["border"], highlightthickness=1)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.sidebar_btns = {}
        self.sidebar_indicator = None
        self._tab_frames = {}
        self._current_tab = None
        self._build_sidebar()

        # 内容区
        content_wrap = tk.Frame(body, bg=t["bg"])
        content_wrap.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.content_frame = tk.Frame(content_wrap, bg=t["bg"])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # 构建所有标签页内容
        self._tab_upload()
        self._tab_update()
        self._tab_branch()
        self._tab_fork()
        self._tab_release()
        self._tab_repos()
        self._tab_search()
        self._tab_issues()
        self._tab_pulls()
        self._tab_webhook()
        self._tab_stats()
        self._tab_settings()
        self._tab_about()

        # 日志面板
        log_lf = ttk.LabelFrame(content_wrap, text=" 操作日志 ", padding=4)
        log_lf.pack(fill=tk.X, side=tk.BOTTOM, padx=8, pady=(0, 6))
        self.log_box = scrolledtext.ScrolledText(log_lf, wrap=tk.WORD,
                                                 font=("Consolas", self.font_size),
                                                 relief=tk.FLAT,
                                                 bg=t["log_bg"], fg=t["log_fg"],
                                                 insertbackground=t["log_fg"],
                                                 selectbackground=t["select_bg"],
                                                 highlightthickness=0, bd=0,
                                                 height=6)
        self.log_box.pack(fill=tk.BOTH, expand=True)
        ttk.Button(log_lf, text="清空",
                   command=lambda: self.log_box.delete("1.0", tk.END)).pack(anchor=tk.E, pady=(4, 0))

        # 底部状态栏
        status_bg = t.get("card_bg", t["bg2"])
        status_bar = tk.Frame(self.root, bg=status_bg,
                              highlightbackground=t["border"], highlightthickness=1)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_lbl = tk.Label(status_bar,
                                   text=f"v{APP_VERSION} | Author: {APP_AUTHOR} | 当前平台: {self.platform}",
                                   bg=status_bg, fg=t["fg3"],
                                   font=("Segoe UI", 8), pady=2)
        self.status_lbl.pack(side=tk.RIGHT, padx=10)

        # 默认显示第一个tab
        self._show_tab("upload")

    def _build_sidebar(self):
        t = self._current_theme
        sidebar_bg = t.get("sidebar_bg", t["bg3"])
        accent = t.get("accent", "#2563eb")

        # Logo 区域
        logo_frame = tk.Frame(self.sidebar, bg=sidebar_bg, height=44)
        logo_frame.pack(fill=tk.X)
        logo_frame.pack_propagate(False)

        tk.Label(logo_frame, text="Code Manager",
                 bg=sidebar_bg, fg=t["fg"],
                 font=("Segoe UI Semibold", self.font_size + 1, "bold")).pack(pady=10)

        # 分隔线
        tk.Frame(self.sidebar, bg=t["border"], height=1).pack(fill=tk.X, padx=12, pady=(4, 4))

        # 导航项
        nav_frame = tk.Frame(self.sidebar, bg=sidebar_bg)
        nav_frame.pack(fill=tk.BOTH, expand=True)

        for emoji_icon, label, tab_id in self.SIDEBAR_ITEMS:
            btn_frame = tk.Frame(nav_frame, bg=sidebar_bg, cursor="hand2", height=36)
            btn_frame.pack(fill=tk.X, padx=6, pady=1)
            btn_frame.pack_propagate(False)

            indicator = tk.Frame(btn_frame, bg=sidebar_bg, width=3)
            indicator.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 0))

            emoji_lbl = tk.Label(btn_frame, text=emoji_icon, bg=sidebar_bg,
                                 fg=t["fg2"], font=("Segoe UI", self.font_size + 2),
                                 width=3, anchor="center")
            emoji_lbl.pack(side=tk.LEFT, padx=(2, 0))

            text_lbl = tk.Label(btn_frame, text=label, bg=sidebar_bg,
                                fg=t["fg2"], font=("Segoe UI", self.font_size),
                                anchor="w")
            text_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 8))

            self.sidebar_btns[tab_id] = {
                "frame": btn_frame,
                "indicator": indicator,
                "emoji": emoji_lbl,
                "text": text_lbl,
            }

            for w in (btn_frame, indicator, emoji_lbl, text_lbl):
                w.bind("<Button-1>", lambda e, tid=tab_id: self._show_tab(tid))
                w.bind("<Enter>", lambda e, tid=tab_id: self._on_sidebar_hover(tid, True))
                w.bind("<Leave>", lambda e, tid=tab_id: self._on_sidebar_hover(tid, False))

        # 底部 spacer
        tk.Frame(nav_frame, bg=sidebar_bg).pack(fill=tk.BOTH, expand=True)

    def _on_sidebar_hover(self, tab_id, entering):
        t = self._current_theme
        sidebar_bg = t.get("sidebar_bg", t["bg3"])

        btn = self.sidebar_btns.get(tab_id)
        if not btn:
            return

        current_tab = getattr(self, '_current_tab', None)
        if current_tab == tab_id:
            return

        if entering:
            hover_bg = t.get("bg3", sidebar_bg)
            btn["frame"].configure(bg=hover_bg)
            btn["indicator"].configure(bg=hover_bg)
            btn["emoji"].configure(bg=hover_bg, fg=t["fg"])
            btn["text"].configure(bg=hover_bg, fg=t["fg"])
        else:
            btn["frame"].configure(bg=sidebar_bg)
            btn["indicator"].configure(bg=sidebar_bg)
            btn["emoji"].configure(bg=sidebar_bg, fg=t["fg2"])
            btn["text"].configure(bg=sidebar_bg, fg=t["fg2"])

    def _show_tab(self, tab_id):
        for tid, frame in self._tab_frames.items():
            frame.pack_forget()
        if tab_id in self._tab_frames:
            self._tab_frames[tab_id].pack(in_=self.content_frame, fill=tk.BOTH, expand=True)
        self._update_sidebar_active(tab_id)
        self._current_tab = tab_id

    def _update_sidebar_active(self, tab_id):
        t = self._current_theme
        sidebar_bg = t.get("sidebar_bg", t["bg3"])
        sidebar_active_bg = t.get("accent", "#2563eb")

        for tid, btn in self.sidebar_btns.items():
            if tid == tab_id:
                btn["frame"].configure(bg=sidebar_active_bg)
                btn["indicator"].configure(bg="#ffffff")
                btn["emoji"].configure(bg=sidebar_active_bg, fg="#ffffff")
                btn["text"].configure(bg=sidebar_active_bg, fg="#ffffff")
            else:
                btn["frame"].configure(bg=sidebar_bg)
                btn["indicator"].configure(bg=sidebar_bg)
                btn["emoji"].configure(bg=sidebar_bg, fg=t["fg2"])
                btn["text"].configure(bg=sidebar_bg, fg=t["fg2"])

    def _card_frame(self, parent, title=None, **kwargs):
        t = self._current_theme
        card = tk.Frame(parent, bg=t.get("card_bg", t["bg2"]),
                        highlightbackground=t.get("card_border", t["border"]),
                        highlightthickness=1, padx=16, pady=12, **kwargs)
        if title:
            ttk.Label(card, text=title,
                      font=("Segoe UI Semibold", self.font_size + 1, "bold"),
                      foreground=t["accent"]).pack(anchor=tk.W, pady=(0, 8))
        return card

    def _make_desc(self, parent, text, row=0, col=0, colspan=3):
        t = self._current_theme
        ttk.Label(parent, text=text, wraplength=580, justify=tk.LEFT,
                  foreground=t["fg2"], font=("Segoe UI", self.font_size)
                  ).grid(row=row, column=col, columnspan=colspan, sticky=tk.W, padx=8, pady=(0, 12))

    def _section_label(self, parent, text, row, col=0, colspan=3):
        t = self._current_theme
        ttk.Label(parent, text=text, font=("Segoe UI Semibold", self.font_size + 1, "bold"),
                  foreground=t["accent"]).grid(row=row, column=col, columnspan=colspan, sticky=tk.W, pady=(16, 8))

    # ─────────────────── 标签页：上传 ───────────────────

    def _tab_upload(self):
        t = self._current_theme
        f = tk.Frame(self.content_frame, bg=t["bg"], padx=12, pady=12)
        self._tab_frames["upload"] = f

        self._make_desc(f,
            "功能说明：将本地项目文件夹上传到GitHub/Gitee。自动创建新仓库，初始化Git，"
            "关联远程地址，提交所有文件并推送。首次上传时可选择开源协议（如MIT、Apache等）。", 0)

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
                                           font=("Segoe UI", self.font_size - 1), wraplength=500)
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
        ttk.Label(f, text=".gitignore模板：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.up_gitignore = tk.StringVar(value="通用")
        gi_cb = ttk.Combobox(f, textvariable=self.up_gitignore,
                              values=list(GITIGNORE_TEMPLATES.keys()), state="readonly", width=10)
        gi_cb.grid(row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        bf = ttk.Frame(f)
        bf.grid(row=r, column=0, columnspan=3, pady=14)
        ttk.Button(bf, text="创建仓库并上传", style="Accent.TButton", command=self._do_upload).pack(side=tk.LEFT, padx=6)
        ttk.Button(bf, text="仅创建远程仓库", command=self._do_create_repo).pack(side=tk.LEFT, padx=6)
        ttk.Button(bf, text="批量上传", command=self._batch_upload).pack(side=tk.LEFT, padx=6)

        f.columnconfigure(1, weight=1)
        self._license_hint()

    def _license_hint(self, event=None):
        key = LICENSES.get(self.up_license.get(), "")
        desc = LICENSE_DESC.get(key, "")
        self.license_hint_lbl.config(text=desc)

    # ─────────────────── 标签页：更新 ───────────────────

    def _tab_update(self):
        t = self._current_theme
        f = tk.Frame(self.content_frame, bg=t["bg"], padx=12, pady=12)
        self._tab_frames["update"] = f

        self._make_desc(f,
            "功能说明：对已关联远程仓库的本地项目进行日常更新。可以将本地修改提交并推送到远程仓库，"
            "也可以从远程拉取最新代码。如果目录还不是Git仓库，可以点击初始化Git按钮。", 0)

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
        self._section_label(f, "初始化与关联（首次使用）", r)
        r += 1
        ttk.Label(f, text="远程仓库地址：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.ud_remote_url = tk.StringVar()
        ttk.Entry(f, textvariable=self.ud_remote_url).grid(row=r, column=1, sticky=tk.EW, pady=4)
        t = self._current_theme
        ttk.Label(f, text="格式：https://github.com/用户名/仓库名.git", foreground=t["fg3"],
                  font=("Segoe UI", self.font_size - 1)).grid(row=r, column=2, sticky=tk.W, padx=4)

        r += 1
        ibf = ttk.Frame(f)
        ibf.grid(row=r, column=0, columnspan=3, sticky=tk.W, pady=4)
        ttk.Button(ibf, text="初始化Git", command=self._init_git).pack(side=tk.LEFT, padx=4)
        ttk.Button(ibf, text="关联远程仓库", command=self._set_remote).pack(side=tk.LEFT, padx=4)
        ttk.Button(ibf, text="初始化并关联（一键）", style="Accent.TButton", command=self._init_and_set_remote).pack(side=tk.LEFT, padx=4)

        r += 1
        self._section_label(f, "提交与推送", r)
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
        t = self._current_theme
        f = tk.Frame(self.content_frame, bg=t["bg"], padx=12, pady=12)
        self._tab_frames["branch"] = f

        self._make_desc(f,
            "功能说明：管理Git分支。分支用于在不影响主线代码的情况下进行开发、测试或修复。"
            "可以从远程加载分支列表，创建新的本地/远程分支，切换当前分支，或删除不再需要的远程分支。", 0)

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
        t = self._current_theme
        f = tk.Frame(self.content_frame, bg=t["bg"], padx=12, pady=12)
        self._tab_frames["fork"] = f

        self._make_desc(f,
            "功能说明：Fork（派生）他人的仓库到你自己的账号下。Fork后你会获得一份独立副本，"
            "可以在自己的副本上自由修改而不影响原仓库。常用于参与开源项目：Fork → 修改 → 提交PR。", 0)

        r = 1
        ttk.Label(f, text="目标仓库：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.fk_repo = tk.StringVar()
        ttk.Entry(f, textvariable=self.fk_repo, width=36).grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)
        t = self._current_theme
        ttk.Label(f, text="格式：用户名/仓库名", foreground=t["fg3"],
                  font=("Segoe UI", self.font_size - 1)).grid(row=r, column=3, sticky=tk.W, padx=4)

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
        ttk.Button(bf, text="批量Fork", command=self._batch_fork).pack(side=tk.LEFT, padx=6)

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
        t = self._current_theme
        f = tk.Frame(self.content_frame, bg=t["bg"], padx=12, pady=12)
        self._tab_frames["release"] = f

        self._make_desc(f,
            "功能说明：创建Release（发布版本），可将源代码打包或上传编译好的软件/文件作为附件。"
            "适用于正式发布版本、提供下载包、记录版本更新日志等场景。"
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
        self.rl_body = scrolledtext.ScrolledText(f, height=5, wrap=tk.WORD, font=("Segoe UI", self.font_size),
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
                  font=("Segoe UI", self.font_size - 1)).grid(row=r, column=1, sticky=tk.W)

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

    # ─────────────────── 标签页：我的仓库 ───────────────────

    def _tab_repos(self):
        t = self._current_theme
        f = tk.Frame(self.content_frame, bg=t["bg"], padx=12, pady=12)
        self._tab_frames["repos"] = f

        self._make_desc(f,
            "功能说明：查看你账号下的所有仓库信息，包括名称、可见性、使用的开源协议、"
            "编程语言和最后更新时间。双击仓库可在浏览器中打开对应页面。", 0)

        r = 1
        bf = ttk.Frame(f)
        bf.grid(row=r, column=0, columnspan=3, sticky=tk.W, pady=4)
        ttk.Button(bf, text="刷新列表", command=self._repos_load).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="浏览器中打开选中仓库", command=self._repos_open).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="导出仓库列表", command=self._export_repos).pack(side=tk.LEFT, padx=4)

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

    # ─────────────────── 标签页：搜索 ───────────────────

    def _tab_search(self):
        t = self._current_theme
        f = tk.Frame(self.content_frame, bg=t["bg"], padx=12, pady=12)
        self._tab_frames["search"] = f

        self._make_desc(f,
            "功能说明：搜索GitHub/Gitee上的开源仓库。可以根据关键词和编程语言筛选，"
            "查看仓库的Star数、Fork数等信息，并快速Fork或克隆感兴趣的仓库。", 0)

        r = 1
        ttk.Label(f, text="搜索关键词：").grid(row=r, column=0, sticky=tk.W, pady=4)
        sf = ttk.Frame(f)
        sf.grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)
        self.sr_query = tk.StringVar()
        ttk.Entry(sf, textvariable=self.sr_query).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(sf, text="搜索", command=self._search_repos).pack(side=tk.LEFT, padx=4)

        r += 1
        ttk.Label(f, text="编程语言：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.sr_lang = tk.StringVar(value="全部")
        lang_cb = ttk.Combobox(f, textvariable=self.sr_lang,
                                values=["全部", "Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript"],
                                state="readonly", width=15)
        lang_cb.grid(row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        self._section_label(f, "搜索结果", r)
        r += 1
        cols = ("仓库名称", "Star", "Fork", "语言", "描述")
        self.sr_tree = ttk.Treeview(f, columns=cols, show="headings", height=12)
        for c in cols:
            self.sr_tree.heading(c, text=c)
        self.sr_tree.column("仓库名称", width=200)
        self.sr_tree.column("Star", width=80, anchor=tk.CENTER)
        self.sr_tree.column("Fork", width=80, anchor=tk.CENTER)
        self.sr_tree.column("语言", width=80, anchor=tk.CENTER)
        self.sr_tree.column("描述", width=300)
        self.sr_tree.grid(row=r, column=0, columnspan=3, sticky=tk.EW, pady=4)
        ssb = ttk.Scrollbar(f, orient=tk.VERTICAL, command=self.sr_tree.yview)
        self.sr_tree.configure(yscrollcommand=ssb.set)
        ssb.grid(row=r, column=3, sticky=tk.NS, pady=4)

        r += 1
        bf = ttk.Frame(f)
        bf.grid(row=r, column=0, columnspan=3, pady=10)
        ttk.Button(bf, text="Fork选中", command=self._sr_fork).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="克隆选中", command=self._sr_clone).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="在浏览器中打开", command=self._sr_open).pack(side=tk.LEFT, padx=4)
        f.columnconfigure(1, weight=1)

    def _search_repos(self):
        if not self._need_auth():
            return
        query = self.sr_query.get().strip()
        if not query:
            messagebox.showwarning("提示", "请输入搜索关键词")
            return
        
        lang = self.sr_lang.get()
        if lang != "全部":
            query = f"{query} language:{lang}"
        
        self._show_loading("正在搜索...")
        def task():
            try:
                repos = self.api.search_repos(query)
                def update():
                    for i in self.sr_tree.get_children():
                        self.sr_tree.delete(i)
                    for r in repos:
                        name = r.get("full_name", "")
                        stars = r.get("stargazers_count", 0)
                        forks = r.get("forks_count", 0)
                        lang = r.get("language", "") or ""
                        desc = (r.get("description", "") or "")[:50]
                        self.sr_tree.insert("", tk.END, values=(name, stars, forks, lang, desc))
                self.root.after(0, update)
                self.logger.add_history("搜索", f"关键词：{query}", self.platform)
                self.log(f"搜索到 {len(repos)} 个仓库")
            except Exception as e:
                self.log(f"搜索失败：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _sr_fork(self):
        sel = self.sr_tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择一个仓库")
            return
        name = self.sr_tree.item(sel[0], "values")[0]
        self.fk_repo.set(name)
        self._show_tab("fork")
        self._do_fork()

    def _sr_clone(self):
        sel = self.sr_tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择一个仓库")
            return
        name = self.sr_tree.item(sel[0], "values")[0]
        self.fk_repo.set(name)
        self._show_tab("fork")

    def _sr_open(self):
        sel = self.sr_tree.selection()
        if not sel:
            return
        name = self.sr_tree.item(sel[0], "values")[0]
        webbrowser.open(f"{PLATFORMS[self.platform]['web']}/{name}")

    # ─────────────────── 标签页：Issue管理 ───────────────────

    def _tab_issues(self):
        t = self._current_theme
        f = tk.Frame(self.content_frame, bg=t["bg"], padx=12, pady=12)
        self._tab_frames["issues"] = f

        self._make_desc(f,
            "功能说明：管理仓库的Issue（问题/任务）。可以查看、创建、关闭Issue，"
            "适用于项目管理、Bug追踪、功能需求等场景。", 0)

        r = 1
        ttk.Label(f, text="仓库 (owner/repo)：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.is_repo_var = tk.StringVar()
        ttk.Entry(f, textvariable=self.is_repo_var, width=28).grid(row=r, column=1, sticky=tk.EW, pady=4)
        ttk.Button(f, text="加载", command=self._load_issues).grid(row=r, column=2, padx=4, pady=4)

        r += 1
        ttk.Label(f, text="状态：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.is_state = tk.StringVar(value="open")
        ttk.Combobox(f, textvariable=self.is_state, values=["open", "closed", "all"],
                      state="readonly", width=10).grid(row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        self._section_label(f, "Issue列表", r)
        r += 1
        cols = ("编号", "标题", "状态", "创建时间")
        self.is_tree = ttk.Treeview(f, columns=cols, show="headings", height=8)
        for c in cols:
            self.is_tree.heading(c, text=c)
        self.is_tree.column("编号", width=60, anchor=tk.CENTER)
        self.is_tree.column("标题", width=300)
        self.is_tree.column("状态", width=80, anchor=tk.CENTER)
        self.is_tree.column("创建时间", width=120, anchor=tk.CENTER)
        self.is_tree.grid(row=r, column=0, columnspan=3, sticky=tk.EW, pady=4)
        isb = ttk.Scrollbar(f, orient=tk.VERTICAL, command=self.is_tree.yview)
        self.is_tree.configure(yscrollcommand=isb.set)
        isb.grid(row=r, column=3, sticky=tk.NS, pady=4)

        r += 1
        self._section_label(f, "创建新Issue", r)
        r += 1
        ttk.Label(f, text="标题：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.is_title = tk.StringVar()
        ttk.Entry(f, textvariable=self.is_title).grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)

        r += 1
        ttk.Label(f, text="内容：").grid(row=r, column=0, sticky=tk.NW, pady=4)
        t = self._current_theme
        self.is_body = scrolledtext.ScrolledText(f, height=4, wrap=tk.WORD, font=("Segoe UI", self.font_size),
                                                  bg=t["entry_bg"], fg=t["entry_fg"],
                                                  insertbackground=t["entry_fg"], highlightthickness=0, bd=1, relief="solid")
        self.is_body.grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)

        r += 1
        ttk.Label(f, text="标签（逗号分隔）：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.is_labels = tk.StringVar()
        ttk.Entry(f, textvariable=self.is_labels).grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)

        r += 1
        bf = ttk.Frame(f)
        bf.grid(row=r, column=0, columnspan=3, pady=10)
        ttk.Button(bf, text="创建Issue", style="Accent.TButton", command=self._create_issue).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="关闭选中Issue", command=self._close_issue).pack(side=tk.LEFT, padx=4)
        f.columnconfigure(1, weight=1)

    def _load_issues(self):
        if not self._need_auth():
            return
        rp = self.is_repo_var.get().strip()
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            messagebox.showwarning("提示", error_msg)
            return
        
        self._show_loading("正在加载Issue列表...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                issues = self.api.list_issues(owner, repo, state=self.is_state.get())
                def update():
                    for i in self.is_tree.get_children():
                        self.is_tree.delete(i)
                    for issue in issues:
                        num = issue.get("number", "")
                        title = issue.get("title", "")
                        state = issue.get("state", "")
                        created = (issue.get("created_at", ""))[:10]
                        self.is_tree.insert("", tk.END, values=(num, title, state, created))
                self.root.after(0, update)
                self.log(f"加载了 {len(issues)} 个Issue")
            except Exception as e:
                self.log(f"加载Issue失败：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _create_issue(self):
        if not self._need_auth():
            return
        rp = self.is_repo_var.get().strip()
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            messagebox.showwarning("提示", error_msg)
            return
        title = self.is_title.get().strip()
        if not title:
            messagebox.showwarning("提示", "请输入Issue标题")
            return
        
        self._show_loading("正在创建Issue...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                body = self.is_body.get("1.0", tk.END).strip()
                labels = [l.strip() for l in self.is_labels.get().split(",") if l.strip()]
                resp = self.api.create_issue(owner, repo, title, body, labels if labels else None)
                if resp.status_code == 201:
                    self.log(f"Issue创建成功：{resp.json().get('html_url', '')}")
                    self.logger.add_history("创建Issue", f"{rp}#{resp.json().get('number', '')}", self.platform, rp)
                    self.root.after(0, self._load_issues)
                else:
                    self.log(f"创建失败：{resp.status_code}")
            except Exception as e:
                self.log(f"创建Issue异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _close_issue(self):
        if not self._need_auth():
            return
        sel = self.is_tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择一个Issue")
            return
        rp = self.is_repo_var.get().strip()
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            return
        
        issue_num = self.is_tree.item(sel[0], "values")[0]
        if not self._confirm_dialog("确认关闭", f"确定要关闭Issue #{issue_num}吗？"):
            return
        
        self._show_loading("正在关闭Issue...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                resp = self.api.close_issue(owner, repo, issue_num)
                if resp.status_code == 200:
                    self.log(f"Issue #{issue_num} 已关闭")
                    self.root.after(0, self._load_issues)
                else:
                    self.log(f"关闭失败：{resp.status_code}")
            except Exception as e:
                self.log(f"关闭Issue异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    # ─────────────────── 标签页：PR管理 ───────────────────

    def _tab_pulls(self):
        t = self._current_theme
        f = tk.Frame(self.content_frame, bg=t["bg"], padx=12, pady=12)
        self._tab_frames["pulls"] = f

        self._make_desc(f,
            "功能说明：管理仓库的Pull Request（拉取请求）。可以查看、创建、合并、关闭PR，"
            "适用于代码审查、协作开发等场景。", 0)

        r = 1
        ttk.Label(f, text="仓库 (owner/repo)：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.pr_repo_var = tk.StringVar()
        ttk.Entry(f, textvariable=self.pr_repo_var, width=28).grid(row=r, column=1, sticky=tk.EW, pady=4)
        ttk.Button(f, text="加载", command=self._load_pulls).grid(row=r, column=2, padx=4, pady=4)

        r += 1
        ttk.Label(f, text="状态：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.pr_state = tk.StringVar(value="open")
        ttk.Combobox(f, textvariable=self.pr_state, values=["open", "closed", "all"],
                      state="readonly", width=10).grid(row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        self._section_label(f, "PR列表", r)
        r += 1
        cols = ("编号", "标题", "状态", "分支")
        self.pr_tree = ttk.Treeview(f, columns=cols, show="headings", height=8)
        for c in cols:
            self.pr_tree.heading(c, text=c)
        self.pr_tree.column("编号", width=60, anchor=tk.CENTER)
        self.pr_tree.column("标题", width=250)
        self.pr_tree.column("状态", width=80, anchor=tk.CENTER)
        self.pr_tree.column("分支", width=200)
        self.pr_tree.grid(row=r, column=0, columnspan=3, sticky=tk.EW, pady=4)
        psb = ttk.Scrollbar(f, orient=tk.VERTICAL, command=self.pr_tree.yview)
        self.pr_tree.configure(yscrollcommand=psb.set)
        psb.grid(row=r, column=3, sticky=tk.NS, pady=4)

        r += 1
        self._section_label(f, "创建新PR", r)
        r += 1
        ttk.Label(f, text="标题：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.pr_title = tk.StringVar()
        ttk.Entry(f, textvariable=self.pr_title).grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)

        r += 1
        ttk.Label(f, text="源分支：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.pr_head = tk.StringVar()
        ttk.Entry(f, textvariable=self.pr_head, width=20).grid(row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        ttk.Label(f, text="目标分支：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.pr_base = tk.StringVar(value="main")
        ttk.Entry(f, textvariable=self.pr_base, width=20).grid(row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        ttk.Label(f, text="内容：").grid(row=r, column=0, sticky=tk.NW, pady=4)
        t = self._current_theme
        self.pr_body = scrolledtext.ScrolledText(f, height=4, wrap=tk.WORD, font=("Segoe UI", self.font_size),
                                                  bg=t["entry_bg"], fg=t["entry_fg"],
                                                  insertbackground=t["entry_fg"], highlightthickness=0, bd=1, relief="solid")
        self.pr_body.grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)

        r += 1
        bf = ttk.Frame(f)
        bf.grid(row=r, column=0, columnspan=3, pady=10)
        ttk.Button(bf, text="创建PR", style="Accent.TButton", command=self._create_pull).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="合并选中PR", command=self._merge_pull).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="关闭选中PR", command=self._close_pull).pack(side=tk.LEFT, padx=4)
        f.columnconfigure(1, weight=1)

    def _load_pulls(self):
        if not self._need_auth():
            return
        rp = self.pr_repo_var.get().strip()
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            messagebox.showwarning("提示", error_msg)
            return
        
        self._show_loading("正在加载PR列表...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                pulls = self.api.list_pulls(owner, repo, state=self.pr_state.get())
                def update():
                    for i in self.pr_tree.get_children():
                        self.pr_tree.delete(i)
                    for pr in pulls:
                        num = pr.get("number", "")
                        title = pr.get("title", "")
                        state = pr.get("state", "")
                        head = pr.get("head", {}).get("ref", "")
                        base = pr.get("base", {}).get("ref", "")
                        branch = f"{head} → {base}"
                        self.pr_tree.insert("", tk.END, values=(num, title, state, branch))
                self.root.after(0, update)
                self.log(f"加载了 {len(pulls)} 个PR")
            except Exception as e:
                self.log(f"加载PR失败：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _create_pull(self):
        if not self._need_auth():
            return
        rp = self.pr_repo_var.get().strip()
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            messagebox.showwarning("提示", error_msg)
            return
        title = self.pr_title.get().strip()
        head = self.pr_head.get().strip()
        if not title or not head:
            messagebox.showwarning("提示", "请输入PR标题和源分支")
            return
        
        self._show_loading("正在创建PR...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                base = self.pr_base.get().strip() or "main"
                body = self.pr_body.get("1.0", tk.END).strip()
                resp = self.api.create_pull(owner, repo, title, head, base, body)
                if resp.status_code == 201:
                    self.log(f"PR创建成功：{resp.json().get('html_url', '')}")
                    self.logger.add_history("创建PR", f"{rp}#{resp.json().get('number', '')}", self.platform, rp)
                    self.root.after(0, self._load_pulls)
                else:
                    self.log(f"创建失败：{resp.status_code}")
            except Exception as e:
                self.log(f"创建PR异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _merge_pull(self):
        if not self._need_auth():
            return
        sel = self.pr_tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择一个PR")
            return
        rp = self.pr_repo_var.get().strip()
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            return
        
        pr_num = self.pr_tree.item(sel[0], "values")[0]
        if not self._confirm_dialog("确认合并", f"确定要合并PR #{pr_num}吗？"):
            return
        
        self._show_loading("正在合并PR...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                resp = self.api.merge_pull(owner, repo, pr_num)
                if resp.status_code == 200:
                    self.log(f"PR #{pr_num} 已合并")
                    self.root.after(0, self._load_pulls)
                else:
                    self.log(f"合并失败：{resp.status_code}")
            except Exception as e:
                self.log(f"合并PR异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _close_pull(self):
        if not self._need_auth():
            return
        sel = self.pr_tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择一个PR")
            return
        rp = self.pr_repo_var.get().strip()
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            return
        
        pr_num = self.pr_tree.item(sel[0], "values")[0]
        if not self._confirm_dialog("确认关闭", f"确定要关闭PR #{pr_num}吗？"):
            return
        
        self._show_loading("正在关闭PR...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                resp = self.api.close_pull(owner, repo, pr_num)
                if resp.status_code == 200:
                    self.log(f"PR #{pr_num} 已关闭")
                    self.root.after(0, self._load_pulls)
                else:
                    self.log(f"关闭失败：{resp.status_code}")
            except Exception as e:
                self.log(f"关闭PR异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    # ─────────────────── 标签页：Webhook ───────────────────

    def _tab_webhook(self):
        t = self._current_theme
        f = tk.Frame(self.content_frame, bg=t["bg"], padx=12, pady=12)
        self._tab_frames["webhook"] = f

        self._make_desc(f,
            "功能说明：配置仓库的Webhook（网络钩子）。当仓库发生特定事件时，"
            "GitHub/Gitee会向指定URL发送HTTP请求，常用于CI/CD、自动化通知等场景。", 0)

        r = 1
        ttk.Label(f, text="仓库 (owner/repo)：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.wh_repo_var = tk.StringVar()
        ttk.Entry(f, textvariable=self.wh_repo_var, width=28).grid(row=r, column=1, sticky=tk.EW, pady=4)
        ttk.Button(f, text="加载", command=self._load_webhooks).grid(row=r, column=2, padx=4, pady=4)

        r += 1
        self._section_label(f, "已有Webhook", r)
        r += 1
        cols = ("ID", "URL", "事件", "状态")
        self.wh_tree = ttk.Treeview(f, columns=cols, show="headings", height=6)
        for c in cols:
            self.wh_tree.heading(c, text=c)
        self.wh_tree.column("ID", width=80, anchor=tk.CENTER)
        self.wh_tree.column("URL", width=350)
        self.wh_tree.column("事件", width=150)
        self.wh_tree.column("状态", width=80, anchor=tk.CENTER)
        self.wh_tree.grid(row=r, column=0, columnspan=3, sticky=tk.EW, pady=4)
        wsb = ttk.Scrollbar(f, orient=tk.VERTICAL, command=self.wh_tree.yview)
        self.wh_tree.configure(yscrollcommand=wsb.set)
        wsb.grid(row=r, column=3, sticky=tk.NS, pady=4)

        r += 1
        self._section_label(f, "创建新Webhook", r)
        r += 1
        ttk.Label(f, text="URL：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.wh_url = tk.StringVar()
        ttk.Entry(f, textvariable=self.wh_url).grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)

        r += 1
        ttk.Label(f, text="事件：").grid(row=r, column=0, sticky=tk.NW, pady=4)
        ef = ttk.Frame(f)
        ef.grid(row=r, column=1, columnspan=2, sticky=tk.W, pady=4)
        self.wh_push = tk.BooleanVar(value=True)
        self.wh_pr = tk.BooleanVar(value=False)
        self.wh_release = tk.BooleanVar(value=False)
        self.wh_issues = tk.BooleanVar(value=False)
        ttk.Checkbutton(ef, text="push", variable=self.wh_push).pack(side=tk.LEFT, padx=4)
        ttk.Checkbutton(ef, text="pull_request", variable=self.wh_pr).pack(side=tk.LEFT, padx=4)
        ttk.Checkbutton(ef, text="release", variable=self.wh_release).pack(side=tk.LEFT, padx=4)
        ttk.Checkbutton(ef, text="issues", variable=self.wh_issues).pack(side=tk.LEFT, padx=4)

        r += 1
        ttk.Label(f, text="密钥（可选）：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.wh_secret = tk.StringVar()
        ttk.Entry(f, textvariable=self.wh_secret, show="*").grid(row=r, column=1, columnspan=2, sticky=tk.EW, pady=4)

        r += 1
        bf = ttk.Frame(f)
        bf.grid(row=r, column=0, columnspan=3, pady=10)
        ttk.Button(bf, text="创建Webhook", style="Accent.TButton", command=self._create_webhook).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="测试选中", command=self._test_webhook).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="删除选中", command=self._delete_webhook).pack(side=tk.LEFT, padx=4)
        f.columnconfigure(1, weight=1)

    def _load_webhooks(self):
        if not self._need_auth():
            return
        rp = self.wh_repo_var.get().strip()
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            messagebox.showwarning("提示", error_msg)
            return
        
        self._show_loading("正在加载Webhook列表...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                hooks = self.api.list_webhooks(owner, repo)
                def update():
                    for i in self.wh_tree.get_children():
                        self.wh_tree.delete(i)
                    for hook in hooks:
                        hook_id = hook.get("id", "")
                        url = hook.get("config", {}).get("url", "")
                        events = ", ".join(hook.get("events", []))
                        active = "启用" if hook.get("active") else "禁用"
                        self.wh_tree.insert("", tk.END, values=(hook_id, url, events, active))
                self.root.after(0, update)
                self.log(f"加载了 {len(hooks)} 个Webhook")
            except Exception as e:
                self.log(f"加载Webhook失败：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _create_webhook(self):
        if not self._need_auth():
            return
        rp = self.wh_repo_var.get().strip()
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            messagebox.showwarning("提示", error_msg)
            return
        url = self.wh_url.get().strip()
        if not url:
            messagebox.showwarning("提示", "请输入Webhook URL")
            return
        
        events = []
        if self.wh_push.get():
            events.append("push")
        if self.wh_pr.get():
            events.append("pull_request")
        if self.wh_release.get():
            events.append("release")
        if self.wh_issues.get():
            events.append("issues")
        if not events:
            events = ["push"]
        
        self._show_loading("正在创建Webhook...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                secret = self.wh_secret.get().strip()
                resp = self.api.create_webhook(owner, repo, url, events, secret)
                if resp.status_code == 201:
                    self.log(f"Webhook创建成功")
                    self.logger.add_history("创建Webhook", url, self.platform, rp)
                    self.root.after(0, self._load_webhooks)
                else:
                    self.log(f"创建失败：{resp.status_code}")
            except Exception as e:
                self.log(f"创建Webhook异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _test_webhook(self):
        if not self._need_auth():
            return
        sel = self.wh_tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择一个Webhook")
            return
        rp = self.wh_repo_var.get().strip()
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            return
        
        hook_id = self.wh_tree.item(sel[0], "values")[0]
        self._show_loading("正在测试Webhook...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                resp = self.api.test_webhook(owner, repo, hook_id)
                if resp.status_code == 204:
                    self.log("Webhook测试成功")
                else:
                    self.log(f"测试失败：{resp.status_code}")
            except Exception as e:
                self.log(f"测试Webhook异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _delete_webhook(self):
        if not self._need_auth():
            return
        sel = self.wh_tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择一个Webhook")
            return
        rp = self.wh_repo_var.get().strip()
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            return
        
        hook_id = self.wh_tree.item(sel[0], "values")[0]
        if not self._confirm_dialog("确认删除", f"确定要删除Webhook {hook_id}吗？"):
            return
        
        self._show_loading("正在删除Webhook...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                resp = self.api.delete_webhook(owner, repo, hook_id)
                if resp.status_code == 204:
                    self.log(f"Webhook {hook_id} 已删除")
                    self.root.after(0, self._load_webhooks)
                else:
                    self.log(f"删除失败：{resp.status_code}")
            except Exception as e:
                self.log(f"删除Webhook异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    # ─────────────────── 标签页：统计 ───────────────────

    def _tab_stats(self):
        t = self._current_theme
        f = tk.Frame(self.content_frame, bg=t["bg"], padx=12, pady=12)
        self._tab_frames["stats"] = f

        self._make_desc(f,
            "功能说明：查看仓库统计数据，包括仓库总数、Star总数、语言分布等信息。", 0)

        r = 1
        ttk.Button(f, text="刷新统计", command=self._load_stats).grid(row=r, column=0, sticky=tk.W, pady=4)

        r += 1
        self._section_label(f, "总览", r)
        r += 1
        t = self._current_theme
        self.stats_overview = ttk.Label(f, text="点击刷新加载统计数据",
                                         font=("Segoe UI", self.font_size),
                                         foreground=t["fg2"])
        self.stats_overview.grid(row=r, column=0, columnspan=2, sticky=tk.W, pady=4)

        r += 1
        self._section_label(f, "语言分布", r)
        r += 1
        self.stats_lang_frame = ttk.Frame(f)
        self.stats_lang_frame.grid(row=r, column=0, columnspan=2, sticky=tk.EW, pady=4)

        r += 1
        self._section_label(f, "最近更新", r)
        r += 1
        self.stats_recent = scrolledtext.ScrolledText(f, height=10, wrap=tk.WORD, font=("Consolas", self.font_size),
                                                       relief=tk.FLAT, bg=t["log_bg"], fg=t["log_fg"],
                                                       insertbackground=t["log_fg"], selectbackground=t["select_bg"],
                                                       highlightthickness=0, bd=0)
        self.stats_recent.grid(row=r, column=0, columnspan=2, sticky=tk.EW, pady=4)
        f.columnconfigure(0, weight=1)

    def _load_stats(self):
        if not self._need_auth():
            return
        self._show_loading("正在加载统计数据...")
        def task():
            try:
                repos = self.api.list_repos()
                
                # 统计数据
                total = len(repos)
                public = sum(1 for r in repos if not r.get("private"))
                private = total - public
                total_stars = sum(r.get("stargazers_count", 0) for r in repos)
                total_forks = sum(r.get("forks_count", 0) for r in repos)
                
                # 语言统计
                languages = {}
                for r in repos:
                    lang = r.get("language") or "未知"
                    languages[lang] = languages.get(lang, 0) + 1
                
                # 最近更新
                recent = sorted(repos, key=lambda x: x.get("updated_at", ""), reverse=True)[:10]
                
                def update():
                    # 总览
                    overview = f"仓库总数：{total}    公开：{public}    私有：{private}\n"
                    overview += f"总Star：{total_stars:,}    总Fork：{total_forks:,}"
                    self.stats_overview.config(text=overview)
                    
                    # 语言分布
                    for widget in self.stats_lang_frame.winfo_children():
                        widget.destroy()
                    sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:8]
                    for lang, count in sorted_langs:
                        percent = count / total * 100 if total > 0 else 0
                        row = ttk.Frame(self.stats_lang_frame)
                        row.pack(fill=tk.X, pady=2)
                        ttk.Label(row, text=f"{lang:12}", width=12).pack(side=tk.LEFT)
                        bar = ttk.Frame(row)
                        bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
                        ttk.Label(bar, text=f"{'█' * int(percent / 5)}", foreground=self._current_theme["accent"]).pack(side=tk.LEFT)
                        ttk.Label(row, text=f"{count} ({percent:.1f}%)", width=12).pack(side=tk.RIGHT)
                    
                    # 最近更新
                    self.stats_recent.delete("1.0", tk.END)
                    for r in recent:
                        name = r.get("full_name", "")
                        updated = (r.get("updated_at", ""))[:10]
                        stars = r.get("stargazers_count", 0)
                        self.stats_recent.insert(tk.END, f"{name:40} ⭐{stars:6}  {updated}\n")
                
                self.root.after(0, update)
                self.logger.add_history("查看统计", f"共{total}个仓库", self.platform)
                self.log("统计数据加载完成")
            except Exception as e:
                self.log(f"加载统计数据失败：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    # ─────────────────── 标签页：设置 ───────────────────

    def _tab_settings(self):
        t = self._current_theme
        f = tk.Frame(self.content_frame, bg=t["bg"], padx=12, pady=12)
        self._tab_frames["settings"] = f

        r = 0
        self._section_label(f, "网络设置", r)
        r += 1
        ttk.Label(f, text="代理地址：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.st_proxy = tk.StringVar(value=self.proxy)
        ttk.Entry(f, textvariable=self.st_proxy, width=40).grid(row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        ttk.Label(f, text="超时时间（秒）：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.st_timeout = tk.StringVar(value=str(self.timeout))
        ttk.Entry(f, textvariable=self.st_timeout, width=10).grid(row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        self._section_label(f, "配置文件管理", r)
        r += 1
        ttk.Label(f, text="当前配置：").grid(row=r, column=0, sticky=tk.W, pady=4)
        pf = ttk.Frame(f)
        pf.grid(row=r, column=1, sticky=tk.W, pady=4)
        self.st_profile = tk.StringVar(value=self.current_profile)
        profiles = self.config_mgr.list_profiles()
        ttk.Combobox(pf, textvariable=self.st_profile, values=profiles,
                      state="readonly", width=15).pack(side=tk.LEFT)
        ttk.Button(pf, text="切换", command=self._switch_profile).pack(side=tk.LEFT, padx=4)
        ttk.Button(pf, text="新建", command=self._new_profile).pack(side=tk.LEFT, padx=4)
        ttk.Button(pf, text="删除", command=self._delete_profile).pack(side=tk.LEFT, padx=4)

        r += 1
        bf = ttk.Frame(f)
        bf.grid(row=r, column=1, sticky=tk.W, pady=4)
        ttk.Button(bf, text="导出配置", command=self._export_config).pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="导入配置", command=self._import_config).pack(side=tk.LEFT, padx=4)

        r += 1
        self._section_label(f, "Git设置", r)
        r += 1
        ttk.Label(f, text="默认.gitignore模板：").grid(row=r, column=0, sticky=tk.W, pady=4)
        self.st_gitignore = tk.StringVar(value="通用")
        ttk.Combobox(f, textvariable=self.st_gitignore, values=list(GITIGNORE_TEMPLATES.keys()),
                      state="readonly", width=10).grid(row=r, column=1, sticky=tk.W, pady=4)

        r += 1
        self._section_label(f, "日志设置", r)
        r += 1
        lbf = ttk.Frame(f)
        lbf.grid(row=r, column=1, sticky=tk.W, pady=4)
        ttk.Button(lbf, text="打开日志目录", command=self._open_log_dir).pack(side=tk.LEFT, padx=4)
        ttk.Button(lbf, text="清空历史记录", command=self._clear_history).pack(side=tk.LEFT, padx=4)

        r += 1
        ttk.Button(f, text="保存设置", style="Accent.TButton", command=self._save_settings).grid(
            row=r, column=1, sticky=tk.W, pady=16)

    def _switch_profile(self):
        profile = self.st_profile.get()
        self.cfg = self.config_mgr.load_profile(profile)
        self.current_profile = profile
        self.cfg["current_profile"] = profile
        save_config(self.cfg, profile)
        self.log(f"已切换到配置：{profile}")
        self._refresh()

    def _new_profile(self):
        name = simpledialog.askstring("新建配置", "请输入配置名称：")
        if name:
            self.config_mgr.save_profile(name, {})
            self.log(f"已创建配置：{name}")
            profiles = self.config_mgr.list_profiles()
            self.st_profile.config(values=profiles)

    def _delete_profile(self):
        profile = self.st_profile.get()
        if profile == "default":
            messagebox.showwarning("提示", "不能删除默认配置")
            return
        if self._confirm_dialog("确认删除", f"确定要删除配置 {profile} 吗？"):
            self.config_mgr.delete_profile(profile)
            self.log(f"已删除配置：{profile}")
            profiles = self.config_mgr.list_profiles()
            self.st_profile.config(values=profiles)
            self.st_profile.set("default")

    def _export_config(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            title="导出配置"
        )
        if path:
            self.config_mgr.export_config(path, self.current_profile)
            self.log(f"配置已导出到：{path}")

    def _import_config(self):
        path = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json")],
            title="导入配置"
        )
        if path:
            self.config_mgr.import_config(path, self.current_profile)
            self.cfg = self.config_mgr.load_profile(self.current_profile)
            self.log(f"配置已导入：{path}")
            self._refresh()

    def _open_log_dir(self):
        os.startfile(LOGS_DIR)

    def _clear_history(self):
        if self._confirm_dialog("确认清空", "确定要清空所有历史记录吗？"):
            self.logger.clear_history()
            self.log("历史记录已清空")

    def _save_settings(self):
        self.proxy = self.st_proxy.get().strip()
        try:
            self.timeout = int(self.st_timeout.get())
        except:
            self.timeout = 30
        
        self.cfg["proxy"] = self.proxy
        self.cfg["timeout"] = self.timeout
        save_config(self.cfg, self.current_profile)
        
        self.log("设置已保存")
        messagebox.showinfo("提示", "设置已保存，部分设置需要重启生效")

    # ─────────────────── 标签页：关于 ───────────────────

    def _tab_about(self):
        t = self._current_theme
        f = tk.Frame(self.content_frame, bg=t["bg"], padx=12, pady=12)
        self._tab_frames["about"] = f

        if self._icon_small:
            ttk.Label(f, image=self._icon_small).grid(row=0, column=0, columnspan=2, pady=(10, 6))

        ttk.Label(f, text=f"{APP_NAME} v{APP_VERSION}",
                  font=("Segoe UI", 14, "bold"),
                  foreground=t["accent"]).grid(row=1, column=0, columnspan=2, pady=4)

        ttk.Label(f, text="GitHub / Gitee 本地代码管理工具",
                  font=("Segoe UI", 10),
                  foreground=t["fg2"]).grid(row=2, column=0, columnspan=2, pady=2)

        ttk.Separator(f, orient=tk.HORIZONTAL).grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=10)

        info_frame = ttk.Frame(f)
        info_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=20)

        ttk.Label(info_frame, text="开发者：", font=("Segoe UI", 10, "bold"),
                  foreground=t["fg"]).grid(row=0, column=0, sticky=tk.W, pady=3)
        ttk.Label(info_frame, text=APP_AUTHOR, font=("Segoe UI", 10),
                  foreground=t["fg"]).grid(row=0, column=1, sticky=tk.W, pady=3, padx=8)

        ttk.Label(info_frame, text="版本号：", font=("Segoe UI", 10, "bold"),
                  foreground=t["fg"]).grid(row=1, column=0, sticky=tk.W, pady=3)
        ttk.Label(info_frame, text=f"v{APP_VERSION}", font=("Segoe UI", 10),
                  foreground=t["fg"]).grid(row=1, column=1, sticky=tk.W, pady=3, padx=8)

        ttk.Label(info_frame, text="Python：", font=("Segoe UI", 10, "bold"),
                  foreground=t["fg"]).grid(row=2, column=0, sticky=tk.W, pady=3)
        ttk.Label(info_frame, text=f"{sys.version.split()[0]}", font=("Segoe UI", 10),
                  foreground=t["fg"]).grid(row=2, column=1, sticky=tk.W, pady=3, padx=8)

        ttk.Separator(f, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=10)

        ttk.Label(f, text="v9.0 新增功能",
                  font=("Segoe UI", 11, "bold"),
                  foreground=t["accent"]).grid(row=6, column=0, columnspan=2, pady=(4, 6))

        features = [
            "• 网络请求优化（自动重试、API限流处理、代理支持）",
            "• 日志持久化与操作历史记录",
            "• Issue管理（创建、关闭）",
            "• PR管理（创建、合并、关闭）",
            "• Webhook配置",
            "• 仓库搜索功能",
            "• 统计面板",
            "• 设置页面（多配置文件、导入导出）",
            "• 批量操作（批量上传、批量Fork）",
            "• .gitignore模板选择",
            "• Nuitka加壳保护"
        ]
        for i, feat in enumerate(features):
            ttk.Label(f, text=feat, font=("Segoe UI", 9),
                      foreground=t["fg2"]).grid(row=7+i, column=0, columnspan=2, sticky=tk.W, padx=20)

        ttk.Separator(f, orient=tk.HORIZONTAL).grid(row=18, column=0, columnspan=2, sticky=tk.EW, pady=10)

        ttk.Label(f, text="联系方式 - 微信扫码添加好友",
                  font=("Segoe UI", 11, "bold"),
                  foreground=t["accent"]).grid(row=19, column=0, columnspan=2, pady=(4, 6))

        if self._weixin_small:
            ttk.Label(f, image=self._weixin_small).grid(row=20, column=0, columnspan=2, pady=4)
        else:
            ttk.Label(f, text="[ 微信二维码图片未找到 ]", foreground=t["fg3"]).grid(row=20, column=0, columnspan=2, pady=4)

        f.columnconfigure(0, weight=1)

    # ─────────────────── 平台切换 ───────────────────

    def _on_platform_change(self, event=None):
        self.platform = self.platform_var.get()
        self.cfg["platform"] = self.platform
        save_config(self.cfg, self.current_profile)
        self.api = None
        self.user = None
        self.user_lbl.config(text="未登录")
        self.log(f"已切换到 {self.platform} 平台，请重新设置Token")
        self._update_status_bar()

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
        save_config(self.cfg, self.current_profile)
        self._rebuild_theme()

    def _on_font_change(self, event=None):
        try:
            self.font_size = int(self.font_var.get())
        except ValueError:
            return
        self.cfg["font_size"] = self.font_size
        save_config(self.cfg, self.current_profile)
        self._rebuild_theme()

    def _on_dark_toggle(self):
        self.dark_mode = self.dark_var.get()
        self.cfg["dark_mode"] = self.dark_mode
        save_config(self.cfg, self.current_profile)
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
        labels = {
            "bg": "主背景色", "fg": "主文字色", "accent": "强调色",
            "btn_bg": "按钮背景", "btn_fg": "按钮文字",
            "entry_bg": "输入框背景", "entry_fg": "输入框文字",
            "tree_bg": "列表背景", "tree_fg": "列表文字",
        }

        main_frame = ttk.Frame(d, padding=12)
        main_frame.pack(fill=tk.BOTH, expand=True)

        row = 0
        ttk.Label(main_frame, text="自定义配色（点击色块选择颜色）",
                  font=("Segoe UI", 11, "bold"),
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

        def apply_custom():
            for key, var in color_vars.items():
                val = var.get().strip()
                if val.startswith("#") and len(val) == 7:
                    self.custom_colors[mode][key] = val
            self.cfg["custom_colors"] = self.custom_colors
            self.theme_name = "自定义"
            self.cfg["theme"] = "自定义"
            save_config(self.cfg, self.current_profile)
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
                  font=("Segoe UI", self.font_size + 1),
                  background=t["bg2"], foreground=t["fg"]).pack(padx=16, pady=(16, 4), anchor=tk.W)
        tv = tk.StringVar(value=self.cfg.get(f"token_{self.platform}", self.cfg.get("token", "")))
        ttk.Entry(d, textvariable=tv, width=58, show="•").pack(padx=16, fill=tk.X)
        ttk.Label(d, text=note, foreground=t["fg3"],
                  font=("Segoe UI", self.font_size - 1),
                  background=t["bg2"]).pack(padx=16, pady=4, anchor=tk.W)

        def ok():
            token = tv.get().strip()
            if not token:
                messagebox.showwarning("提示", "请输入Token", parent=d)
                return
            self._set_token(token)
            self.cfg[f"token_{self.platform}"] = token
            save_config(self.cfg, self.current_profile)
            d.destroy()

        ttk.Button(d, text="保存", style="Accent.TButton", command=ok).pack(pady=14)

    def _set_token(self, token):
        self.api = PlatformAPI(self.platform, token, logger=self.logger, proxy=self.proxy, timeout=self.timeout)
        u = self.api.get_user()
        if u:
            self.user = u
            self.user_lbl.config(text=f"[{self.platform}] 已登录：{u['login']}")
            self.logger.log(f"认证成功：{u['login']} ({u.get('email', 'N/A')})")
            self.logger.log(f"Token: {mask_token(token)}")
            self.logger.add_history("登录", f"{self.platform} - {u['login']}", self.platform)
        else:
            self.user_lbl.config(text=f"[{self.platform}] 认证失败")
            self.logger.log("Token认证失败，请检查Token是否正确或已过期")

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

    def _browse_assets(self):
        files = filedialog.askopenfilenames(title="选择要上传的文件")
        if files:
            self.rl_assets_var.set(";".join(files))

    # ─────────────────── 上传 ───────────────────

    def _do_upload(self):
        if not self._need_auth():
            return
        path = self.up_path.get().strip()
        name = self.up_name.get().strip()
        if not path or not os.path.isdir(path):
            messagebox.showerror("错误", "请选择有效的本地项目路径")
            return
        
        is_valid, error_msg = validate_repo_name(name)
        if not is_valid:
            messagebox.showerror("输入错误", error_msg)
            return
        
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
                gitignore_template = self.up_gitignore.get()

                # 创建.gitignore
                if gitignore_template:
                    self.git.create_gitignore(path, gitignore_template)

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

                username = self.user.get("login", "user")
                email = self.user.get("email") or f"{username}@users.noreply.com"
                if email == "N/A":
                    email = f"{username}@users.noreply.com"
                self.git.set_user_info(path, username, email)
                self.git.remote(path, clone_url)
                self.git.ensure_branch(path, target_branch)

                if resp.status_code == 201 and lic:
                    self.git._run(["pull", "origin", target_branch, "--allow-unrelated-histories", "--no-edit"], cwd=path)
                    self.git.add_all(path)
                    self.git.commit(path, msg)
                elif resp.status_code == 201 and not lic:
                    self.git.add_all(path)
                    ok_c, _, _ = self.git.commit(path, msg)
                    if not ok_c:
                        self.log("没有新的更改需要提交")

                ok, _, _ = self.git.push(path, "origin", target_branch)
                if ok:
                    self.log("上传完成！")
                    self._repos_cache.append({"path": path, "name": name, "url": html_url})
                    self.cfg["local_repos"] = self._repos_cache
                    save_config(self.cfg, self.current_profile)
                    self.logger.add_history("上传代码", f"{name}", self.platform, name)
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
                    self.logger.add_history("创建仓库", name, self.platform, name)
                elif resp.status_code == 422:
                    self.log(f"仓库 {name} 已存在")
                else:
                    self.log(f"创建失败：{resp.status_code} {resp.text}")
            except Exception as e:
                self.log(f"创建异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)

        threading.Thread(target=task, daemon=True).start()

    def _batch_upload(self):
        """批量上传多个项目"""
        folders = filedialog.askdirectories(title="选择多个项目文件夹")
        if not folders:
            return
        
        if not self._need_auth():
            return
        
        def task():
            success = 0
            fail = 0
            for folder in folders:
                name = os.path.basename(folder)
                self.log(f"开始上传：{name}")
                try:
                    # 创建仓库
                    resp = self.api.create_repo(name, auto_init=False)
                    if resp.status_code in (201, 422):
                        if resp.status_code == 201:
                            data = resp.json()
                            clone_url = self.api.get_clone_url(data)
                        else:
                            data = self.api.get_repo(self.user["login"], name).json()
                            clone_url = self.api.get_clone_url(data)
                        
                        # Git操作
                        if not self.git.is_repo(folder):
                            self.git.init(folder)
                        self.git.remote(folder, clone_url)
                        self.git.add_all(folder)
                        self.git.commit(folder, "Initial commit")
                        ok, _, _ = self.git.push(folder, "origin", "main")
                        if ok:
                            self.log(f"{name} 上传成功")
                            success += 1
                        else:
                            self.log(f"{name} 推送失败")
                            fail += 1
                    else:
                        self.log(f"{name} 创建仓库失败：{resp.status_code}")
                        fail += 1
                except Exception as e:
                    self.log(f"{name} 上传异常：{e}")
                    fail += 1
            
            self.log(f"批量上传完成：成功 {success}，失败 {fail}")
            self.root.after(0, self._hide_loading)
        
        self._show_loading("正在批量上传...")
        threading.Thread(target=task, daemon=True).start()

    # ─────────────────── 更新 ───────────────────

    def _do_commit_push(self):
        path = self.ud_path.get().strip()
        if not path or not os.path.isdir(path):
            messagebox.showerror("错误", "请选择有效的本地项目路径")
            return
        
        if not self.git.is_repo(path):
            messagebox.showerror("错误", "所选目录不是Git仓库\n\n请先初始化Git或选择已有的Git仓库")
            return
        
        branch = self.ud_branch.get().strip() or "main"
        is_valid, error_msg = validate_branch_name(branch)
        if not is_valid:
            messagebox.showerror("输入错误", f"分支名无效：{error_msg}")
            return
        
        self._show_loading("正在提交并推送...")

        def task():
            try:
                msg = self.ud_msg.get().strip() or "Update"
                self.log(f"正在提交到 {path}...")
                self.git.add_all(path)
                self.git.commit(path, msg)
                # 获取当前分支名
                current_branch = self.git.current_branch(path)
                if current_branch:
                    self.log(f"当前分支：{current_branch}")
                    # 如果本地分支是 master 但用户输入的是 main，先重命名分支
                    if current_branch == "master" and branch == "main":
                        self.log("重命名分支 master -> main")
                        self.git.rename_branch(path, "master", "main")
                        current_branch = "main"
                else:
                    current_branch = branch
                
                # 先尝试拉取远程代码（处理远程已有内容的情况）
                self.log("正在同步远程仓库...")
                pull_ok, _, _ = self.git._run(["pull", "origin", current_branch, "--allow-unrelated-histories", "--no-edit"], cwd=path)
                if not pull_ok:
                    self.log("拉取失败，可能是冲突，尝试强制合并...")
                    self.git._run(["pull", "origin", current_branch, "--allow-unrelated-histories", "--no-edit", "-X", "theirs"], cwd=path)
                
                # 添加所有文件并提交
                self.git.add_all(path)
                self.git.commit(path, msg)
                
                self.log(f"正在推送到 {current_branch}...")
                ok, _, _ = self.git.push(path, "origin", current_branch, force=self.ud_force.get())
                if ok:
                    self.log("推送完成！")
                    self.logger.add_history("推送代码", f"分支：{current_branch}", self.platform)
                else:
                    # 推送失败，尝试强制推送
                    self.log("推送失败，尝试强制推送...")
                    ok2, _, _ = self.git.push(path, "origin", current_branch, force=True)
                    if ok2:
                        self.log("强制推送成功！")
                        self.logger.add_history("推送代码", f"分支：{current_branch}（强制）", self.platform)
                    else:
                        self.log("推送失败，请检查网络和权限")
            except Exception as e:
                self.log(f"操作异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _do_commit(self):
        path = self.ud_path.get().strip()
        if not path:
            messagebox.showerror("错误", "请选择本地项目路径")
            return
        if not self.git.is_repo(path):
            messagebox.showerror("错误", "所选目录不是Git仓库")
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
            messagebox.showerror("错误", "请选择本地项目路径")
            return
        if not self.git.is_repo(path):
            messagebox.showerror("错误", "所选目录不是Git仓库")
            return
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
            messagebox.showerror("错误", "请选择本地项目路径")
            return
        if not self.git.is_repo(path):
            messagebox.showerror("错误", "所选目录不是Git仓库")
            return
        branch = self.ud_branch.get().strip() or "main"
        is_valid, error_msg = validate_branch_name(branch)
        if not is_valid:
            messagebox.showerror("输入错误", f"分支名无效：{error_msg}")
            return
        self._show_loading("正在拉取远程代码...")
        def task():
            try:
                ok, msg = self.git.pull_with_conflict_check(path, "origin", branch)
                if ok:
                    self.log("拉取完成")
                else:
                    self.log(f"拉取失败：{msg}")
            except Exception as e:
                self.log(f"拉取异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _init_git(self):
        path = self.ud_path.get().strip()
        if not path:
            messagebox.showerror("错误", "请先选择本地项目路径")
            return
        if not os.path.isdir(path):
            messagebox.showerror("错误", "所选路径不是有效的目录")
            return
        if self.git.is_repo(path):
            messagebox.showinfo("提示", "该目录已经是Git仓库，无需重复初始化")
            return
        self._show_loading("正在初始化Git...")
        def task():
            try:
                ok, _, _ = self.git.init(path)
                if ok:
                    self.log(f"Git初始化成功：{path}")
                    self.git.add_all(path)
                    self.git.commit(path, "Initial commit")
                    self.log("已创建初始提交")
                    self.logger.add_history("初始化Git", path, self.platform)
                    self.root.after(0, lambda: messagebox.showinfo("成功", "Git初始化完成！"))
                else:
                    self.log("Git初始化失败")
            except Exception as e:
                self.log(f"初始化异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _set_remote(self):
        path = self.ud_path.get().strip()
        if not path:
            messagebox.showerror("错误", "请先选择本地项目路径")
            return
        if not self.git.is_repo(path):
            messagebox.showerror("错误", "所选目录不是Git仓库，请先初始化Git")
            return
        remote_url = self.ud_remote_url.get().strip()
        if not remote_url:
            messagebox.showerror("错误", "请输入远程仓库地址")
            return
        self._show_loading("正在关联远程仓库...")
        def task():
            try:
                ok, _, _ = self.git.remote(path, remote_url)
                if ok:
                    self.log(f"远程仓库关联成功：{remote_url}")
                    self.logger.add_history("关联远程仓库", remote_url, self.platform)
                    self.root.after(0, lambda: messagebox.showinfo("成功", "远程仓库关联成功！"))
                else:
                    self.log("关联远程仓库失败")
            except Exception as e:
                self.log(f"关联异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _init_and_set_remote(self):
        path = self.ud_path.get().strip()
        if not path:
            messagebox.showerror("错误", "请先选择本地项目路径")
            return
        if not os.path.isdir(path):
            messagebox.showerror("错误", "所选路径不是有效的目录")
            return
        remote_url = self.ud_remote_url.get().strip()
        if not remote_url:
            messagebox.showerror("错误", "请输入远程仓库地址")
            return
        self._show_loading("正在初始化并关联远程仓库...")
        def task():
            try:
                if not self.git.is_repo(path):
                    self.log("正在初始化Git...")
                    ok, _, _ = self.git.init(path)
                    if not ok:
                        self.log("Git初始化失败")
                        return
                    self.log("Git初始化成功")
                self.log("正在关联远程仓库...")
                ok, _, _ = self.git.remote(path, remote_url)
                if ok:
                    self.log(f"远程仓库关联成功：{remote_url}")
                else:
                    self.log("关联远程仓库失败")
                    return
                if not self.git.has_commits(path):
                    self.log("正在创建初始提交...")
                    self.git.add_all(path)
                    self.git.commit(path, "Initial commit")
                    self.log("初始提交创建成功")
                
                # 确保分支名为 main
                current_branch = self.git.current_branch(path)
                if current_branch and current_branch != "main":
                    self.log(f"重命名分支 {current_branch} -> main")
                    self.git.rename_branch(path, current_branch, "main")
                self.logger.add_history("初始化并关联", f"{path} -> {remote_url}", self.platform)
                self.root.after(0, lambda: messagebox.showinfo("成功", "初始化完成！现在可以提交并推送代码。"))
            except Exception as e:
                self.log(f"操作异常：{e}")
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
        is_valid, error_msg = validate_branch_name(nb)
        if not is_valid:
            messagebox.showerror("输入错误", f"分支名无效：{error_msg}")
            return
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
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            messagebox.showerror("输入错误", error_msg)
            return
        nb = self.br_new.get().strip()
        is_valid, error_msg = validate_branch_name(nb)
        if not is_valid:
            messagebox.showerror("输入错误", f"分支名无效：{error_msg}")
            return
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
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            return
        sel = self.br_list.curselection()
        if not sel:
            messagebox.showwarning("提示", "请先选择一个分支")
            return
        br = self.br_list.get(sel[0])
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
                    self.logger.add_history("Fork仓库", rp, self.platform, rp)
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
                self.log(f"克隆完成：{lp}")
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

    def _batch_fork(self):
        """批量Fork仓库"""
        if not self._need_auth():
            return
        sel = self.fk_list.curselection()
        if not sel:
            messagebox.showwarning("提示", "请先选择要Fork的仓库（可多选）")
            return
        
        repos = [self.fk_list.get(i).split("  ")[0].strip() for i in sel]
        
        def task():
            success = 0
            fail = 0
            for rp in repos:
                try:
                    owner, repo = rp.split("/", 1)
                    self.log(f"正在Fork：{rp}...")
                    resp = self.api.fork_repo(owner, repo)
                    if resp.status_code in (202, 201, 200):
                        self.log(f"{rp} Fork成功")
                        success += 1
                    else:
                        self.log(f"{rp} Fork失败：{resp.status_code}")
                        fail += 1
                except Exception as e:
                    self.log(f"{rp} Fork异常：{e}")
                    fail += 1
            
            self.log(f"批量Fork完成：成功 {success}，失败 {fail}")
            self.root.after(0, self._hide_loading)
        
        self._show_loading("正在批量Fork...")
        threading.Thread(target=task, daemon=True).start()

    # ─────────────────── Release ───────────────────

    def _do_release(self):
        if not self._need_auth():
            return
        if self.platform != "GitHub":
            messagebox.showinfo("提示", "Release功能目前仅支持GitHub平台")
            return
        rp = self.rl_repo.get().strip()
        is_valid, error_msg = validate_owner_repo(rp)
        if not is_valid:
            messagebox.showerror("输入错误", error_msg)
            return
        tag = self.rl_tag.get().strip()
        if not tag:
            messagebox.showerror("错误", "请输入Tag名称")
            return
        
        self._show_loading("正在创建Release...")
        def task():
            try:
                owner, repo = rp.split("/", 1)
                self.log(f"验证仓库 {rp} 是否存在...")
                repo_resp = self.api.get_repo(owner, repo)
                if repo_resp.status_code == 404:
                    self.log(f"错误：仓库 {rp} 不存在或无访问权限")
                    return
                elif repo_resp.status_code != 200:
                    self.log(f"验证仓库失败：{repo_resp.status_code}")
                    return
                
                self.log(f"仓库验证通过，开始创建Release...")
                title = self.rl_title.get().strip() or tag
                body = self.rl_body.get("1.0", tk.END).strip()
                resp = self.api.create_release(owner, repo, tag, title, body, self.rl_draft.get(), self.rl_pre.get())
                if resp.status_code == 201:
                    rd = resp.json()
                    self.log(f"Release 创建成功: {rd['html_url']}")
                    self.logger.add_history("创建Release", f"{rp} - {tag}", self.platform, rp)
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
                elif resp.status_code == 422:
                    error_detail = resp.json().get("message", "")
                    self.log(f"创建失败：数据验证错误 - {error_detail}")
                else:
                    self.log(f"创建失败: {resp.status_code}")
            except Exception as e:
                self.log(f"创建Release异常：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

    def _list_releases(self):
        if not self._need_auth():
            return
        rp = self.rl_repo.get().strip()
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

    def _export_repos(self):
        """导出仓库列表"""
        if not self._need_auth():
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("CSV", "*.csv")],
            title="导出仓库列表"
        )
        if not file_path:
            return
        
        self._show_loading("正在导出仓库列表...")
        def task():
            try:
                repos = self.api.list_repos()
                
                if file_path.endswith(".csv"):
                    with open(file_path, "w", encoding="utf-8-sig", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow(["仓库名称", "可见性", "开源协议", "语言", "Star", "Fork", "最后更新"])
                        for r in repos:
                            vis = "私有" if r["private"] else "公开"
                            lang = r.get("language") or ""
                            lic = ""
                            if r.get("license"):
                                lic = r["license"].get("spdx_id", "")
                            stars = r.get("stargazers_count", 0)
                            forks = r.get("forks_count", 0)
                            updated = (r.get("updated_at", ""))[:10]
                            writer.writerow([r["full_name"], vis, lic, lang, stars, forks, updated])
                else:
                    export_data = []
                    for r in repos:
                        export_data.append({
                            "name": r.get("full_name", ""),
                            "private": r.get("private", False),
                            "language": r.get("language", ""),
                            "stars": r.get("stargazers_count", 0),
                            "forks": r.get("forks_count", 0),
                            "url": r.get("html_url", ""),
                            "updated": (r.get("updated_at", ""))[:10]
                        })
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                self.log(f"仓库列表已导出到：{file_path}")
                self.logger.add_history("导出仓库列表", f"{len(repos)}个仓库", self.platform)
            except Exception as e:
                self.log(f"导出失败：{e}")
            finally:
                self.root.after(0, self._hide_loading)
        threading.Thread(target=task, daemon=True).start()

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

