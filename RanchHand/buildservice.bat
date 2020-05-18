pyinstaller -y -F --hiddenimport win32timezone -i "..\common\images\KRNC.ico"  ".\RanchHandService.py"

del .\RanchHandService.spec