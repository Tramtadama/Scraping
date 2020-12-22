#!/bin/sh

. myenv/bin/activate
cp input/data.csv ../scraping/data.csv
cd ../scraping
python3 hornbach_sraper.py
python3 hornbach_sraper.py --mode sk
rm hornbach_urls.txt prices.txt data.csv
rm -r sraped/*

