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

main_link = 'https://www.baumax.cz/vyhledvn/szukaj.html?szukaj='
data = pd.read_csv('data.csv', sep=";")
cz_data = data.loc[data['COUNTRY'] == 'CZ']
cz_data = cz_data.drop(cz_data.loc[cz_data['EAN'] == 0].index.values)
ean_list = cz_data['EAN'].to_list()
print(ean_list)
print("exit")
exit()
options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(options=options)

redirected_urls = []
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

    print(driver.current_url)
    redirected_urls.append(driver.current_url)
