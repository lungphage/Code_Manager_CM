@echo off
chcp 65001 >nul
echo ==========================================
echo   Code Manager v10.1 - Nuitka?????? (Windows)
echo   Author: LZF
echo ==========================================
echo.

echo [1/4] ??????Python??????...
..\venv\Scripts\python.exe --version
echo.

echo [2/4] ????????????...
..\venv\Scripts\pip.exe install requests nuitka ordered-set --quiet
echo.

echo [3/4] Nuitka?????????...
..\venv\Scripts\python.exe -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-disable-console ^
    --windows-icon-from-ico=..\icon.ico ^
    --include-data-file=..\icon.png=icon.png ^
    --include-data-file=..\weixin.png=weixin.png ^
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
pause
