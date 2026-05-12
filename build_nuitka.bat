@echo off
chcp 65001 >nul
echo ==========================================
<<<<<<< HEAD
echo   Code Manager v10.1 - Nuitka?????? (Windows)
=======
echo   Code Manager v9.6 - Nuitka构建 (Windows)
>>>>>>> 95dbcf97ef60c11fc4ba3c45ce338ee56369b655
echo   Author: LZF
echo ==========================================
echo.

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
>>>>>>> 95dbcf97ef60c11fc4ba3c45ce338ee56369b655
..\venv\Scripts\python.exe -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-disable-console ^
    --windows-icon-from-ico=..\icon.ico ^
    --include-data-file=..\icon.png=icon.png ^
    --include-data-file=..\weixin.png=weixin.png ^
<<<<<<< HEAD
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

echo [4/4] 构建完成！
echo   EXE位置：dist\CodeManager_v9_6.exe
>>>>>>> 95dbcf97ef60c11fc4ba3c45ce338ee56369b655
pause
