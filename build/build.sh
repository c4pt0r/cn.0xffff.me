#!/bin/sh
# Build script for Vercel

# make sure wget is installed
yum install wget

# get saait
wget https://codemadness.org/releases/saait/saait-0.8.tar.gz
tar zxvf ./saait-0.8.tar.gz
cd saait-0.8; make; cd .. 

# check if saait successfuly built

if [ -f ./saait-0.8/saait ]; then
    export PATH=./saait-0.8:$PATH
else
    echo "saait build failed"
    exit 1
fi

mkdir -p output
find ../pages -type f -name '*.cfg' -print0 | sort -zr | xargs -0 saait -t ../templates -c ../config.cfg
cp ../style.css ../print.css ../public.asc output/

# copy to public directory
cp -r ./output ../public
