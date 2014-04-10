# Dota 2 Mod - Mana cost for items

This mod adds mana/health cost to the icons of in-game items.
E.g. Soul Ring, TP, Refresher Orb, etc.
There are also additional modification to upgradeable items and Power threads, indicating their level or the next stat.
The images are made by Reddit user **/u/lerobotsexy**, who also originally came up with the idea for this mod.

This repo contains a bunch of script that will automatically generate the icon images.

## Download

https://github.com/rossengeorgiev/dota2mod_manacost/releases

## Building
### Required tools
* HLExtract `Windows x86/x64` `Included`
* Pathon w/ Imaging library
* `optional` bash
* `optional`  zip

### Steps
1. Make sure the correct path is set in `fetch_src_files.bat`
2. Run `fetch_src_files.bat`, which will all item images and items.txt schema in `./src/`
3. Run `render_icons.py`, will find all items that have mana/health cost, render the new files and then place them in `./items/`
4. `optional` Create a release zip file with `build_release.sh`
