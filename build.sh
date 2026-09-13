#!/bin/bash

rm -rf source

mkdir -p source

cp main.py source/
cp README.md source/
cp requirements.txt source/
cp run.sh source/

cp -R assets source/

makepkg -si
