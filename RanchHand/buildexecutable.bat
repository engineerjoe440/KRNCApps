pyinstaller -y -wF -i "..\common\images\KRNC.ico"  ".\RanchHand.py"
pyinstaller -y -F --hiddenimport win32timezone -i "..\common\images\KRNC.ico"  ".\RanchHandService.py"
pyinstaller -y -F  ".\updateinstaller.py"


del /S /Q .\build\

del .\RanchHand.spec
del .\RanchHandService.spec
del .\updateinstaller.spec