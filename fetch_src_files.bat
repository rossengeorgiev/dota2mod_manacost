@echo off

echo "Clearing old sources files"

del /F /S /Q .\src\*

echo "Extracting item.txt"

.\tools\hlextract\x64\HLExtract.exe -p "D:\Steam\steamapps\common\dota 2 beta\dota\pak01_dir.vpk" -d .\src -e "root\scripts\npc\items.txt"

echo "Extraing images for all items.txt"

.\tools\hlextract\x64\HLExtract.exe -p "D:\Steam\steamapps\common\dota 2 beta\dota\pak01_dir.vpk" -d .\src -e "root\resource\flash3\images\items"

