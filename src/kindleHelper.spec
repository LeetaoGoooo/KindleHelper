# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['kindleHelper.py', 'ui/app.py', 'ui/__init__.py', 'tools/__init__.py', 'tools/download.py', 'tools/fake_user_agent.py', 'tools/ksend.py', 'exceptions/__init__.py', 'exceptions/configException.py', 'exceptions/ksendException.py', 'exceptions/websiteException.py', 'website/__init__.py', 'website/lanjuhua.py', 'website/pdfhome.py', 'website/ziliaoh.py', 'website/kg.py','widgets/downloaded.py', 'widgets/downloading.py', 'widgets/progressbar.py', 'widgets/send.py', 'widgets/systray.py', 'worker/__init__.py', 'worker/download.py', 'worker/search.py', 'worker/send.py'],
             pathex=['/Users/leetao/Workspace/py/kindlehelper'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='kindleHelper',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='logo.ico')
app = BUNDLE(exe,
             name='kindleHelper.app',
             icon='logo.ico',
             bundle_identifier=None)
