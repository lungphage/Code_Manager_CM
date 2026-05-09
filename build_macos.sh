#!/bin/bash
# ==========================================
#   Code Manager v9.6 - Nuitka构建 (macOS)
#   Author: LZF
# ==========================================

set -e

echo "=========================================="
echo "  Code Manager v9.6 - Nuitka构建 (macOS)"
echo "  Author: LZF"
echo "=========================================="
echo ""

# 检查Python版本
echo "[1/5] 检查Python版本..."
python3 --version
echo ""

# 创建虚拟环境（如果不存在）
if [ ! -d "../venv" ]; then
    echo "[2/5] 创建虚拟环境..."
    python3 -m venv ../venv
else
    echo "[2/5] 虚拟环境已存在"
fi
echo ""

# 激活虚拟环境并安装依赖
echo "[3/5] 安装依赖..."
source ../venv/bin/activate
pip install requests nuitka ordered-set --quiet
echo ""

# Nuitka编译
echo "[4/5] Nuitka编译中..."
python3 -m nuitka \
    --standalone \
    --onefile \
    --macos-create-app-bundle \
    --include-data-file=../icon.png=icon.png \
    --include-data-file=../weixin.png=weixin.png \
    --output-filename=CodeManager_v9_6 \
    --company-name="LZF" \
    --product-name="Code Manager" \
    --file-version=9.6.0 \
    --product-version=9.6.0 \
    --enable-plugin=tk-inter \
    --nofollow-import-to=test_release \
    --assume-yes-for-downloads \
    github_manager_v9.6.py

echo ""
echo "[5/5] 构建完成！"
echo "  应用位置：dist/CodeManager_v9_6.app"
echo "  或者：dist/CodeManager_v9_6 (命令行版本)"
