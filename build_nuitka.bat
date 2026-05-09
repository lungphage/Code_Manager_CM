@echo off
chcp 65001 >nul
echo ==========================================
<<<<<<< HEAD
echo   Code Manager v9.6 - Nuitka构建
=======
<<<<<<< HEAD
echo   Code Manager v9.5 - Nuitka??
=======
<<<<<<< HEAD
echo   Code Manager v9.4 - Nuitka??
=======
echo   Code Manager v8.0 - Nuitka??
>>>>>>> 9f1342512d62e0ee06fa527768887d64140cb558
>>>>>>> f62eff4bc9cac51c13060ce3ab3c90497d3cb6aa
>>>>>>> 7249cb9a7b20d00a0c4e65ec81790cbca4518779
echo   Author: LZF
echo ==========================================
echo.

<<<<<<< HEAD
echo [1/4] 检查Python版本...
.venv\Scripts\python.exe --version
echo.

echo [2/4] 安装依赖...
.venv\Scripts\pip.exe install requests nuitka ordered-set --quiet
echo.

echo [3/4] Nuitka编译中...
=======
echo [1/4] ??Python??...
.venv\Scripts\python.exe --version
echo.

echo [2/4] ????...
.venv\Scripts\pip.exe install requests nuitka ordered-set --quiet
echo.

<<<<<<< HEAD
echo [3/4] Nuitka???...
=======
<<<<<<< HEAD
echo [3/4] Nuitka???...
=======
echo [3/4] Nuitka?????5-10?????????...
>>>>>>> 9f1342512d62e0ee06fa527768887d64140cb558
>>>>>>> f62eff4bc9cac51c13060ce3ab3c90497d3cb6aa
>>>>>>> 7249cb9a7b20d00a0c4e65ec81790cbca4518779
.venv\Scripts\python.exe -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-disable-console ^
    --windows-icon-from-ico=icon.ico ^
    --include-data-file=icon.png=icon.png ^
    --include-data-file=weixin.png=weixin.png ^
<<<<<<< HEAD
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
=======
<<<<<<< HEAD
    --output-filename=CodeManager_v9_5.exe ^
    --company-name="LZF" ^
    --product-name="Code Manager" ^
    --file-version=9.5.0 ^
    --product-version=9.5.0 ^
    --enable-plugin=tk-inter ^
    --nofollow-import-to=test_release ^
    --assume-yes-for-downloads ^
    github_manager_v9.5.py
echo.

echo [4/4] ?????
echo   EXE???dist\CodeManager_v9_5.exe
=======
<<<<<<< HEAD
    --output-filename=CodeManager_v9_4.exe ^
    --company-name="LZF" ^
    --product-name="Code Manager" ^
    --file-version=9.4.0 ^
    --product-version=9.4.0 ^
    --enable-plugin=tk-inter ^
    --nofollow-import-to=test_release ^
    --assume-yes-for-downloads ^
    github_manager_v9.4.py
echo.

echo [4/4] ?????
echo   EXE???dist\CodeManager_v9_4.exe
=======
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
>>>>>>> 9f1342512d62e0ee06fa527768887d64140cb558
>>>>>>> f62eff4bc9cac51c13060ce3ab3c90497d3cb6aa
>>>>>>> 7249cb9a7b20d00a0c4e65ec81790cbca4518779
pause
