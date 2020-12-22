#!/bin/sh

cp input/data.csv ../sikoNew/sikoNew/data.csv
cd ../sikoNew/sikoNew
python3 siko_scraper.py
scrapy crawl siko -o siko.json
python3 siko_postprocess.py

rm ean_to_url.json siko.json siko_found_eans.txt siko_not_found_eans.txt
rm siko_urls.txt
python3 siko_scraper.py --mode 'sk'
scrapy crawl siko -o siko.json
python3 siko_postprocess.py --mode 'sk'
rm ean_to_url.json siko.json siko_found_eans.txt siko_not_found_eans.txt
rm siko_urls.txt data.csv
