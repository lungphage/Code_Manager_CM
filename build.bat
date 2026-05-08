@echo off
chcp 65001 >nul
echo ==========================================
echo   Code Manager v7.1 - 构建EXE
echo   Author: LZF
echo ==========================================
echo.

echo [1/3] 检查依赖...
python -c "import requests" 2>nul
if %errorlevel% neq 0 (
    python -m pip install requests --quiet
)
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    python -m pip install pyinstaller --quiet
)
echo 依赖检查完成.
echo.

echo [2/3] 打包中...
python -m PyInstaller --noconfirm --onefile --windowed ^
    --name "CodeManager_v7_1" ^
    --icon icon.ico ^
    --add-data "icon.png;." ^
    --add-data "weixin.png;." ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    --exclude-module PIL ^
    --exclude-module scipy ^
    --exclude-module PyQt5 ^
    --exclude-module PyQt6 ^
    --exclude-module django ^
    --exclude-module flask ^
    --exclude-module IPython ^
    --exclude-module notebook ^
    --exclude-module pytest ^
    --exclude-module setuptools ^
    --exclude-module pkg_resources ^
    github_manager_v7.py

if %errorlevel% neq 0 (
    echo.
    echo 打包失败！
    pause
    exit /b 1
)

echo.
echo [3/3] 构建完成！
echo   EXE 位置：dist\CodeManager_v7_1.exe
echo.
if exist dist\CodeManager_v7_1.exe (
    for %%A in (dist\CodeManager_v7_1.exe) do echo   文件大小：%%~zA 字节
)
echo.
pause
