@echo off
chcp 65001 >nul
echo ==========================================
echo   Code Manager v8.0 - Nuitka??
echo   Author: LZF
echo ==========================================
echo.

echo [1/4] ??Python??...
.venv\Scripts\python.exe --version
echo.

echo [2/4] ????...
.venv\Scripts\pip.exe install requests nuitka ordered-set --quiet
echo.

echo [3/4] Nuitka?????5-10?????????...
.venv\Scripts\python.exe -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-disable-console ^
    --windows-icon-from-ico=icon.ico ^
    --include-data-file=icon.png=icon.png ^
    --include-data-file=weixin.png=weixin.png ^
    --output-filename=CodeManager_v8_0.exe ^
    --company-name="LZF" ^
    --product-name="Code Manager" ^
    --file-version=8.0.0 ^
    --product-version=8.0.0 ^
    --enable-plugin=tk-inter ^
    --nofollow-import-to=test_release ^
    github_manager_v8.py
echo.

echo [4/4] ?????
echo   EXE???dist\CodeManager_v8_0.exe
if exist dist\CodeManager_v8_0.exe (
    for %%A in (dist\CodeManager_v8_0.exe) do echo   ?????%%~zA ??
)
echo.
pause
