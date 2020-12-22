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
import json

parser = argparse.ArgumentParser()
parser.add_argument('--mode', type=str, default='cz')
args = parser.parse_args()


if args.mode == 'sk':
    print('mode sk')
    main_link = 'https://www.siko.sk/search?text='
    data = pd.read_csv('data.csv', sep=";")
    cz_data = data.loc[data['COUNTRY'] == 'SK']
    cz_data = cz_data.drop(cz_data.loc[cz_data['EAN'] == 0].index.values)
    ean_list = cz_data['EAN'].to_list()
else:
    print('mode cz')
    main_link = 'https://www.siko.cz/search?text='
    data = pd.read_csv('data.csv', sep=";")
    cz_data = data.loc[data['COUNTRY'] == 'CZ']
    cz_data = cz_data.drop(cz_data.loc[cz_data['EAN'] == 0].index.values)
    ean_list = cz_data['EAN'].to_list()

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(options=options)

redirected_urls = []
found_eans = []
not_found_eans = []
ean_to_url = {}
for ean in ean_list:
    link = main_link + str(ean)
    driver.get(link)
    
    start = time.time()
    ean_found = True
    while(link == driver.current_url):
        time.sleep(1)
        end = time.time()
        if start-end < -2:
            ean_found = False
            break

    if ean_found:
        found_eans.append(ean)
        redirected_urls.append(driver.current_url)
        ean_to_url[str(ean)] = driver.current_url
    else:
        not_found_eans.append(ean)

with open('siko_urls.txt', 'w') as f:
    for item in redirected_urls:
        f.write("%s\n" %item)

with open('siko_found_eans.txt', 'w') as f:
    for item in found_eans:
        f.write("%s\n" %item)

with open('siko_not_found_eans.txt', 'w') as f:
    for item in not_found_eans:
        f.write("%s\n" %item)

with open('ean_to_url.json', 'w') as f:
    f.write(json.dumps(ean_to_url))
