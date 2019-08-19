# -*- mode: python -*-

# TODO: Get single file build working again.

block_cipher = None
a = Analysis(['chess.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.datas += Tree('images', prefix='images')
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='chess',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
