#!/bin/bash

echo -e "\nAdding untouched prerendered images..."

cp -vn ./prerendered_items/* ./out/items/

echo -e "\nMake a zip file..."

cd ./out/
rm -f *.zip

zip -r -9 mod_item_manacost.zip ./items
zip -r -9 mod_spellicons ./spellicons

echo -e "\nMake showcase images.."

cd ./items
montage -crop 88x64+0+0 -resize 75% `ls` -tile 10 -shadow -geometry "+3+2" -monitor - | convert - -monitor -crop 722x+0+0 ../../showcase_items.png

cd ../spellicons
montage -resize 50% `ls|sort -R|head -30` -tile 10 -shadow -geometry "+4+2" -monitor - | convert - -monitor -crop 722x+0+0 ../../showcase_spellicons.png

echo -e "\nFinished"
