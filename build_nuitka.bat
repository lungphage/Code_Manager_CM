@echo off
chcp 65001 >nul
echo ==========================================
echo   Code Manager v10.4 - Nuitka 构建
echo   Author: LZF
echo ==========================================
echo.

REM ── 优先使用项目 venv，回退到全局 Python ──
set PYTHON=..\venv\Scripts\python.exe
if not exist %PYTHON% (
    echo 未找到虚拟环境，使用全局 Python...
    set PYTHON=python
)

echo [1/4] 检查 Python 版本...
%PYTHON% --version
if %errorlevel% neq 0 (
    echo 错误：未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)
echo.

echo [2/4] 安装依赖...
%PYTHON% -m pip install requests "nuitka[onefile]" ordered-set --quiet
if %errorlevel% neq 0 (
    echo 错误：依赖安装失败
    pause
    exit /b 1
)
echo.

echo [3/4] Nuitka 编译中（首次运行会下载 C 编译器，约需数分钟）...
%PYTHON% -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-console-mode=disable ^
    --windows-icon-from-ico=..\icon.ico ^
    --include-data-file=..\icon.png=icon.png ^
    --include-data-file=..\weixin.png=weixin.png ^
    --output-filename=CodeManager_v10_4.exe ^
    --output-dir=dist ^
    --company-name="LZF" ^
    --product-name="Code Manager" ^
    --file-version=10.4.0 ^
    --product-version=10.4.0 ^
    --file-description="GitHub/Gitee 本地代码管理工具" ^
    --enable-plugin=tk-inter ^
    --nofollow-import-to=test ^
    --assume-yes-for-downloads ^
    github_manager_v10.4.py

if %errorlevel% neq 0 (
    echo 错误：Nuitka 编译失败，请检查上方输出
    pause
    exit /b 1
)
echo.

echo [4/4] 构建完成！
echo   EXE 位置：dist\CodeManager_v10_4.exe
echo.
pause
