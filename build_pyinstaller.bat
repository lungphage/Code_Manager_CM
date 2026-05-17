@echo off
chcp 65001 >nul
echo ==========================================
echo   Code Manager v10.5 - PyInstaller 构建
echo   Author: LZF
echo ==========================================
echo.

echo [1/4] 检查 Python 版本...
python --version
if %errorlevel% neq 0 (
    echo 错误：未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)
echo.

echo [2/4] 安装依赖...
pip install requests pyinstaller --quiet
if %errorlevel% neq 0 (
    echo 错误：依赖安装失败
    pause
    exit /b 1
)
echo.

echo [3/4] PyInstaller 打包中（使用 spec 文件）...
pyinstaller --noconfirm CodeManager.spec
if %errorlevel% neq 0 (
    echo 错误：打包失败，请检查上方输出
    pause
    exit /b 1
)
echo.

echo [4/4] 构建完成！
echo   EXE 位置：dist\CodeManager_v10_5.exe
echo.
pause
