#!/bin/sh

echo -n "Filename (without extension): "
read -r filename

[ -z "$filename" ] && echo "Please enter valid filename" && exit 1

echo -n "Title: "
read -r title

[ -z "$title" ] && echo "Please enter valid title" && exit 1

echo -n "Description: "
read -r description

echo -n "Keyword: "
read -r keywords

today=$(date +%Y-%m-%d)

newfile=$(find pages -type f -name '*.cfg' -print0 | sort -zr | cut -c 7-9 | tail -n2 | awk '{s=$1+1} END {printf "%03d", s}')

cfg_file=pages/$newfile-$filename.cfg
html_file=pages/$newfile-$filename.html

echo "filename = $filename.html" > $cfg_file
echo "title = $title" >> $cfg_file
echo "description = $description" >> $cfg_file
echo "keywords = $keywords" >> $cfg_file
echo "created = $today" >> $cfg_file
echo "updated = $today" >> $cfg_file

echo "<!DOCTYPE html>" > $html_file
echo "<html>" >> $html_file

echo "Done! Now edit $html_file and $cfg_file"
