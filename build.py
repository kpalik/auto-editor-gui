import PyInstaller.__main__
import os
import shutil

project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')

PyInstaller.__main__.run([
    os.path.join(src_path, 'main.py'),
    '--name=AutoEditorGUI',
    '--onefile',
    '--windowed',
    '--icon=assets/icons/app.ico' if os.path.exists('assets/icons/app.ico') else '',
    f'--add-data={os.path.join(src_path, "database", "schema.sql")}{os.pathsep}database',
    '--hidden-import=customtkinter',
    '--hidden-import=PIL',
    '--hidden-import=watchdog',
    '--collect-all=customtkinter',
    '--noconfirm',
    '--clean',
])

print("\nBuild complete! Executable is in the 'dist' folder.")
