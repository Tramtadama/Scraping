from selenium import webdriver
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('--url', default=None, type=str)
args = parser.parse_args()

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(options=options)

link = args.url
driver.get(link)

while(link == driver.current_url):
    time.sleep(1)

redirected_url = driver.current_url
print(redirected_url)
