#!/usr/bin/env bash

set -e

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

cd "$SCRIPT_DIR/.."

BLENDER_ADDON_PATH="./CodeToCADBlenderAddon"
OUTPUT_FILE_PATH="$BLENDER_ADDON_PATH.zip"

# Clean up existing files
echo "Cleaning up existing files."

for  file in $(find ./codetocad -name '*__pycache__') ; do
rm -rf $file
done
for  file in $(find ./providers/blender/ -name '*__pycache__') ; do
rm -rf $file
done
for  file in $(find ./ -name 'CodeToCADBlenderAddon') ; do
    echo "Removed CodeToCADBlenderAddon"
    rm -rf $file
done
for file in $(find ./ -name 'CodeToCADBlenderAddon.zip') ; do
    echo "Removed CodeToCADBlenderAddon.zip"
    rm -rf $file
done


# Copy new files
echo "Copying new files."

mkdir $BLENDER_ADDON_PATH
mkdir -p $BLENDER_ADDON_PATH/providers/blender/blender_provider
cp -r ./providers/blender/blender_provider $BLENDER_ADDON_PATH/providers/blender
cp -r ./codetocad $BLENDER_ADDON_PATH/
cp ./providers/blender/blender_addon.py $BLENDER_ADDON_PATH/__init__.py

# Make blender_provider the main provider in CodeToCAD module
# echo "from blender_provider import *" >> $BLENDER_ADDON_PATH/codetocad/__init__.py

# Write version string
echo "Writing version string."

GIT_EPOCH=$(git show -s --format=%ct HEAD)
echo "GIT EPOCH: $GIT_EPOCH"

echo $GIT_EPOCH > $BLENDER_ADDON_PATH/version.txt

# Zip the BlenderAddon folder
echo "Zipping BlenderAddon folder."

zip -q -r $OUTPUT_FILE_PATH $BLENDER_ADDON_PATH