pyinstaller -y -wF -i "..\common\images\KRNC.ico"  ".\RanchHand.py"
pyinstaller -y -wF --hiddenimport win32timezone -i "..\common\images\KRNC.ico"  ".\RanchHandService.py"
pyinstaller -y -F  ".\updateinstaller.py"

