# -*- mode: python ; coding: utf-8 -*-
# Build: pyinstaller caps_lock_indicator.spec  ->  dist\CapsWin.exe

a = Analysis(
    ['caps_lock_indicator.py'],
    pathex=[],
    binaries=[],
    datas=[],
    # pystray elige el backend en tiempo de ejecución; hay que incluirlo explícitamente.
    hiddenimports=['pystray._win32'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # Módulos que la app no usa: reducen el tamaño del ejecutable.
    excludes=['unittest', 'pydoc', 'doctest', 'test'],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CapsWin',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    # UPX desactivado: reduce falsos positivos de antivirus y el tiempo de arranque.
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
