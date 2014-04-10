#!/bin/bash

echo -e "\nAdd prerendered images..."

cp -v ./prerendered_items/* ./items/

echo -e "\nMake a zip file..."

zip -9 release.zip ./items/*

echo -e "\nFinished"
