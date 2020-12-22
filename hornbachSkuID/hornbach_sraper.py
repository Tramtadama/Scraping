import math
import csv
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import time
from selenium import webdriver
import os
import re
import urllib.request
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--mode', type=str, default='cz')
args = parser.parse_args()


if args.mode == 'sk':
    print('mode sk')
    main_link = 'https://www.hornbach.sk/shop/vyhladavanie/sortiment/'
    data = pd.read_csv('data.csv', sep=";")
    cz_data = data.loc[data['COUNTRY'] == 'SK']
    cz_data = cz_data.drop(cz_data.loc[cz_data['SKU_ID'] == 0].index.values)
    ean_list = cz_data['SKU_ID'].to_list()
    print(ean_list)
else:
    print('mode cz')
    main_link = 'https://www.hornbach.cz/shop/vyhledavani/sortiment/'
    data = pd.read_csv('data.csv', sep=";")
    cz_data = data.loc[data['COUNTRY'] == 'CZ']
    cz_data = cz_data.drop(cz_data.loc[cz_data['SKU_ID'] == 0].index.values)
    ean_list = cz_data['SKU_ID'].to_list()


options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(options=options)

redirected_urls = []
failed_eans = []
succes_eans = {}
for ean in ean_list:
    if not math.isnan(ean):
        ean = int(ean)
        link = main_link + str(ean)
        driver.get(link)
        
        while(link == driver.current_url):
            time.sleep(1)
        print(driver.current_url)
        if "no-results" in driver.current_url:
            failed_eans.append(ean)
        else:
            succes_eans[driver.current_url] = ean
            redirected_urls.append(driver.current_url)

with open('hornbach_urls.txt', 'w') as f:
    for item in redirected_urls:
        f.write("%s\n" % item)
    
files_list = []
final_eans = []
class HornbachSpider(scrapy.Spider):

    name = 'hornbach'

    def start_requests(self):
        
        with open('hornbach_urls.txt') as f:
            urls = f.read().splitlines()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        url_split = response.url.split("/")
        ean = succes_eans[response.url]
        final_eans.append(ean)
        page = url_split[-2]
        product_name = url_split[-3]
        filename = 'sraped/quotes-%s.txt' % page
        if 'no-results' not in filename:
            files_list.append(filename)
        with open(filename, 'wb') as f:
            f.write(product_name.encode())
        self.log('Saved file %s' % filename)

process = CrawlerProcess({'FEED_URI': 'export.json'})
process.crawl(HornbachSpider)
process.start()

#os.remove('sraped/quotes-no-results.txt')
art_list = []

prices = []
names = []
for ean, file in zip(succes_eans, files_list):
        with open(file) as f:
            names.append(f.read())
        art = re.sub("[^\d]", "", file)
        if args.mode == 'sk':
            link = 'https://www.hornbach.sk/mvc/hbprice/article-tracking-prices/%s/0' % art
        else:
            link = 'https://www.hornbach.cz/mvc/hbprice/article-tracking-prices/%s/0' % art
        response = urllib.request.urlopen(link)
        text = response.read()
        text_split = text.decode("utf-8").split(",")
        for split in text_split:
            if "totalPrice" in split:
                price = re.sub("[^\d\.]", "", split)
                prices.append(price)
#        with open(file) as f:
#            print(file, f.read(), ean)

with open('prices.txt', 'w') as f:
    for item in prices:
        f.write("%s\n" % item)

with open('prices.txt', 'rb') as f:
    prices = f.read().splitlines()

prices = [x.decode('utf-8') for x in prices]
empty_names = ["ean nenalezen" for ean in failed_eans]
empty_prices = ["" for ean in failed_eans]

df_succes = pd.DataFrame(list(zip(final_eans, names, prices)), columns=['EAN', 'Nazev', 'Cena'])
df_fail = pd.DataFrame(list(zip(failed_eans, empty_names, empty_prices)), columns=['EAN', 'Nazev', 'Cena'])

print('success')
if args.mode == 'cz':
    df_succes.append(df_fail).to_csv(r'../Scrape/output/HornbachCZ_SKUIDresults.csv', index=False)
else:    
    df_succes.append(df_fail).to_csv(r'../Scrape/output/HornbachSK_SKUIDresults.csv', index=False)
