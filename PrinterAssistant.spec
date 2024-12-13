# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['.venv\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('.venv/data/print_records.csv', '.venv/data'), ('admin_config.json', '.'), ('.venv/logs', 'logs'), ('.venv/data_manager.py', '.'), ('.venv/printer_control.py', '.'), ('.venv/admin_window.py', '.'), ('.venv/gui.py', '.'), ('.venv/app_controller.py', '.')],
    hiddenimports=['tkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='PrinterAssistant',
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
)
