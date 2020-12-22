#!/bin/sh

cp input/data.csv ../merkury/merkury/merkury/spiders/data.csv
cp output/Baumax_results.csv ../merkury/merkury/merkury/spiders/baumax_results.csv
cd ../merkury/merkury/merkury/spiders

python3 merkury_urls.py
scrapy crawl merkury -o merkury_products.json
scrapy crawl product -o merkury_final.json
python3 ../../../merkury_postprocess.py

cp Merkury_results.csv /home/lu/Scraping/Kaja/Scrape/output/Merkury_results.csv
rm baumax_results.csv data.csv merkury_final.json merkury_products.json
rm Merkury_results.csv merkury_urls.json
