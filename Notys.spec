# -*- mode: python ; coding: utf-8 -*-
import sys
import platform
SPECPATH = os.path.dirname(os.path.abspath(__file__)) if 'SPECPATH' not in globals() else SPECPATH
sys.path.append(SPECPATH)
import version

# Detect platform icon
icon_file = 'app_icon.ico' if platform.system() == 'Windows' else 'app_icon.icns'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/icons/*.png', 'assets/icons'), ('logo.png', '.')],
    hiddenimports=['striprtf],
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
    [],
    exclude_binaries=True,
    name='Notys',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,  # <-- Set dynamic icon here
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Notys',
)
app = BUNDLE(
    coll,
    name=f'{version.APP_NAME}.app',
    icon='app_icon.icns',
    bundle_identifier=None,
    info_plist={
        'CFBundleName': version.APP_NAME,
        'CFBundleGetInfoString': version.INFO_STRING,
        'CFBundleVersion': version.VERSION,
        'CFBundleShortVersionString': version.SHORT_VERSION,
        'NSHumanReadableCopyright': version.COPYRIGHT,
    },
)