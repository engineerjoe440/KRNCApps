pyinstaller -y -i ^
 "D:/Files/Stanley Solutions/KRNCApps/UniversalSongBarnManager/images/KRNC.ico" ^
 --add-data "D:/Files/Stanley Solutions/KRNCApps/UniversalSongBarnManager/images";"images/" ^
 -n UniversalSongBarnManager -p ^
 "D:\Files\Stanley Solutions\KRNCApps\UniversalSongBarnManager" ^
 --exclude-module matplotlib  ^
 "D:\Files\Stanley Solutions\KRNCApps\UniversalSongBarnManager\main.pyw"