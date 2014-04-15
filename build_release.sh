#!/bin/bash

echo -e "\nAdd prerendered images..."

cp -vn ./prerendered_items/* ./items/

echo -e "\nMake a zip file..."

rm -f release.zip
zip -9 release.zip ./items/*

echo -e "\nMake showcase image.."

cd ./items
montage -crop 100x64+0+0 `ls` -tile 6 -shadow -geometry "+11+2" -monitor - | convert - -monitor -crop 722x+0+0 ../showcase.png

echo -e "\nFinished"
