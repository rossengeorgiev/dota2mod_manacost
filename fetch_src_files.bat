@echo off
set STEAMDIR="D:\Steam"

echo "Clearing old sources files"

del /F /S /Q .\src\*

echo "Extracting item.txt"

.\tools\hlextract\x64\HLExtract.exe -p "%STEAMDIR%\steamapps\common\dota 2 beta\dota\pak01_dir.vpk" -d .\src -e "root\scripts\npc\items.txt"

echo "Extracting npc_abilities.txt"

.\tools\hlextract\x64\HLExtract.exe -p "%STEAMDIR%\steamapps\common\dota 2 beta\dota\pak01_dir.vpk" -d .\src -e "root\scripts\npc\npc_abilities.txt"

echo "Extraing images for all item icons"

.\tools\hlextract\x64\HLExtract.exe -p "%STEAMDIR%\steamapps\common\dota 2 beta\dota\pak01_dir.vpk" -d .\src -e "root\resource\flash3\images\items"

echo "Extraing images for all spellicons"

.\tools\hlextract\x64\HLExtract.exe -p "%STEAMDIR%\steamapps\common\dota 2 beta\dota\pak01_dir.vpk" -d .\src -e "root\resource\flash3\images\spellicons"

