#!/bin/sh

mkdir -p output
find pages -type f -name '*.cfg' -print0 | sort -zr | xargs -0 saait
cp style.css print.css output/
