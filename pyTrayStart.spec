# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['pyTrayStart\\pyTrayStart.py'],
             pathex=['Z:\\Dev\\Python\\serious\\pyTrayStart'],
             binaries=[],
             datas=[
             ('pyTrayStart/resources/icons/*', 'resources/icons/'),
             ('pyTrayStart/resources/json/*', 'resources/json/'),
             ('pyTrayStart/resources/styles/*', 'resources/styles/'),

             ],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='pyTrayStart',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='pyTrayStart')
