#!/bin/bash

echo -e "\nAdd prerendered images..."

cp -vn ./prerendered_items/* ./items/

echo -e "\nMake a zip file..."

rm -f release.zip
zip -9 release.zip ./items/*

echo -e "\nMake showcase image.."

cd ./items
montage `ls` -geometry "+2+2" -tile 5 ../showcase.png

echo -e "\nFinished"
