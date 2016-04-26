#!/bin/bash

echo -e "\nAdding untouched prerendered images..."

cp -vn ./prerendered_items/* ./out/goldcost/resource/flash3/images/items/
cp -vn ./prerendered_items/* ./out/manacost/resource/flash3/images/items/

echo -e "\nMake a zip file..."

cd ./out/
rm -f *.zip

zip -r -9 mod_manacost.zip costmod_manacost
zip -r -9 mod_goldcost.zip costmod_goldcost
zip -r -9 mod_combined.zip costmod_combined
zip -r -9 mod_damagetype.zip costmod_damagetype

echo -e "\nMake showcase images.."

pushd ./manacost
find . -type f | sort -R | head -30 > ../filelist.txt
montage -crop 88x64+0+0 -resize 75% @../filelist.txt -tile 10 -shadow -geometry "+3+2" -monitor - | convert - -monitor -crop 722x+0+0 ../../showcase_items_manacost.png
popd

pushd ./combined
find . -type f | sort -R | head -30 > ../filelist.txt
montage -crop 88x64+0+0 -resize 75% @../filelist.txt -tile 10 -shadow -geometry "+3+2" -monitor - | convert - -monitor -crop 722x+0+0 ../../showcase_items_combined.png
popd

pushd ./damagetype
find . -type f | sort -R | head -30 > ../filelist.txt
montage -resize 50% @../filelist.txt -tile 10 -shadow -geometry "+4+2" -monitor - | convert - -monitor -crop 722x+0+0 ../../showcase_spellicons.png

rm ../filelist.txt

echo -e "\nFinished"
