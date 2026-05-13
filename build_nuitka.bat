@echo off
chcp 65001 >nul
echo ==========================================
<<<<<<< HEAD
echo   Code Manager v10.3 - Nuitka 构建
=======
<<<<<<< HEAD
<<<<<<< HEAD
echo   Code Manager v10.2 - Nuitka?????? (Windows)
=======
echo   Code Manager v9.6 - Nuitka?????? (Windows)
=======
echo   Code Manager v10.1 - Nuitka?????? (Windows)
=======
echo   Code Manager v9.6 - Nuitka构建 (Windows)
>>>>>>> ace4e701c59cf763d7a6628a7ed050fe49a6fb9b
>>>>>>> 95dbcf97ef60c11fc4ba3c45ce338ee56369b655
>>>>>>> d3f9b3a691e131323a0db6d0cc5ee7aaaa1aa4bd
echo   Author: LZF
echo ==========================================
echo.

<<<<<<< HEAD
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
%PYTHON% -m pip install requests nuitka ordered-set --quiet
if %errorlevel% neq 0 (
    echo 错误：依赖安装失败
    pause
    exit /b 1
)
echo.

echo [3/4] Nuitka 编译中（首次运行会下载 C 编译器，约需数分钟）...
%PYTHON% -m nuitka ^
=======
<<<<<<< HEAD
echo [1/4] ??????Python??????...
..\venv\Scripts\python.exe --version
echo.

echo [2/4] ????????????...
..\venv\Scripts\pip.exe install requests nuitka ordered-set --quiet
echo.

echo [3/4] Nuitka?????????...
=======
<<<<<<< HEAD
echo [1/4] ??????Python??????...
..\venv\Scripts\python.exe --version
echo.

echo [2/4] ????????????...
..\venv\Scripts\pip.exe install requests nuitka ordered-set --quiet
echo.

echo [3/4] Nuitka?????????...
=======
echo [1/4] 检查Python版本...
..\venv\Scripts\python.exe --version
echo.

echo [2/4] 安装依赖...
..\venv\Scripts\pip.exe install requests nuitka ordered-set --quiet
echo.

echo [3/4] Nuitka编译中...
>>>>>>> ace4e701c59cf763d7a6628a7ed050fe49a6fb9b
>>>>>>> 95dbcf97ef60c11fc4ba3c45ce338ee56369b655
..\venv\Scripts\python.exe -m nuitka ^
>>>>>>> d3f9b3a691e131323a0db6d0cc5ee7aaaa1aa4bd
    --standalone ^
    --onefile ^
    --windows-disable-console ^
    --windows-icon-from-ico=..\icon.ico ^
    --include-data-file=..\icon.png=icon.png ^
    --include-data-file=..\weixin.png=weixin.png ^
<<<<<<< HEAD
    --output-filename=CodeManager_v10_3.exe ^
    --output-dir=dist ^
    --company-name="LZF" ^
    --product-name="Code Manager" ^
    --file-version=10.3.0 ^
    --product-version=10.3.0 ^
    --file-description="GitHub/Gitee 本地代码管理工具" ^
    --enable-plugin=tk-inter ^
    --nofollow-import-to=test ^
    --assume-yes-for-downloads ^
    github_manager_v10.3.py

if %errorlevel% neq 0 (
    echo 错误：Nuitka 编译失败，请检查上方输出
    pause
    exit /b 1
)
echo.

echo [4/4] 构建完成！
echo   EXE 位置：dist\CodeManager_v10_3.exe
echo.
=======
<<<<<<< HEAD
<<<<<<< HEAD
    --output-filename=CodeManager_v10_2.exe ^
    --company-name="LZF" ^
    --product-name="Code Manager" ^
    --file-version=10.2.0 ^
    --product-version=10.2.0 ^
    --enable-plugin=tk-inter ^
    --nofollow-import-to=test_release ^
    --assume-yes-for-downloads ^
    github_manager_v10.2.py
echo.

echo [4/4] ???????????????
echo   EXE?????????dist\CodeManager_v10_2.exe
=======
    --output-filename=CodeManager_v10_1.exe ^
    --company-name="LZF" ^
    --product-name="Code Manager" ^
    --file-version=10.1.0 ^
    --product-version=10.1.0 ^
    --enable-plugin=tk-inter ^
    --nofollow-import-to=test_release ^
    --assume-yes-for-downloads ^
    github_manager_v10.1.py
echo.

echo [4/4] ???????????????
echo   EXE?????????dist\CodeManager_v10_1.exe
>>>>>>> ace4e701c59cf763d7a6628a7ed050fe49a6fb9b
=======
    --output-filename=CodeManager_v9_6.exe ^
    --company-name="LZF" ^
    --product-name="Code Manager" ^
    --file-version=9.6.0 ^
    --product-version=9.6.0 ^
    --enable-plugin=tk-inter ^
    --nofollow-import-to=test_release ^
    --assume-yes-for-downloads ^
    github_manager_v9.6.py
echo.

<<<<<<< HEAD
echo [4/4] ???????????????
echo   EXE?????????dist\CodeManager_v9_6.exe
=======
echo [4/4] 构建完成！
echo   EXE位置：dist\CodeManager_v9_6.exe
>>>>>>> ace4e701c59cf763d7a6628a7ed050fe49a6fb9b
>>>>>>> 95dbcf97ef60c11fc4ba3c45ce338ee56369b655
>>>>>>> d3f9b3a691e131323a0db6d0cc5ee7aaaa1aa4bd
pause
