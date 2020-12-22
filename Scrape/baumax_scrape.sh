#!/bin/sh

cp input/data.csv ../baumax/baumax/baumax/spiders/data.csv
cd ../baumax/baumax/baumax/spiders

python3 baumax_make_urls.py
scrapy crawl baumax -o baumax_products.json
scrapy crawl product -o products.json
python3 ../../../baumax_postprocess.py
cp Baumax_results.csv /home/ll/Scraping/Kaja/Scrape/output/Baumax_results.csv
rm Baumax_results.csv baumax_products.json baumax_urls.json data.csv products.json
