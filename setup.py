import sys

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
buildOptions = dict(include_files = ['pyTrayStart/resources'])
buildOptions['include_msvcr'] = True

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI"
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "pyTrayStart",
    version = "0.1",
    description = "A Launcher in your Taskbar",
    options = dict(build_exe = buildOptions),
    executables = [Executable("pyTrayStart\\pyTrayStart.py", base=base)]
)
