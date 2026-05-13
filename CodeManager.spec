# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for CodeManager v10.3

a = Analysis(
    ['github_manager_v10.3.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../icon.png',   '.'),
        ('../weixin.png', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'numpy', 'pandas', 'PIL', 'scipy',
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6',
        'django', 'flask', 'IPython', 'notebook',
        'pytest', 'setuptools', 'pkg_resources',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CodeManager_v10_3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['../icon.ico'],
)
