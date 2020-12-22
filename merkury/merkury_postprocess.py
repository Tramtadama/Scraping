import json
import pandas as pd

with open('merkury_products.json') as f:
    products = json.load(f)

with open('merkury_urls.json') as f:
    urls = json.load(f)

with open('merkury_final.json') as f:
    final = json.load(f)

product_to_url = {}

for fin in final:
    for product in products:
        if product['product_link']:
            if fin['url'] == product['product_link']:
                product_to_url[product['url']] = fin['url']
                
url_to_ean = {}
for pro in product_to_url:
    for url in urls:
        if pro == url:
            url_to_ean[url] = urls[url] 


product_to_ean = {}
for prod_key, prod_value in product_to_url.items():
    for url_key, url_value in url_to_ean.items():
        if prod_key == url_key:
            product_to_ean[prod_value] = url_value

for fin in final:
    for pro, ean in product_to_ean.items():
        if fin['url'] == pro:
            fin['ean'] = ean


names = []
prices = []
codes = []
eans = []

for fin in final:
    for key, value in fin.items():
        if key == 'name':
            names.append(value)
        if key == 'price':
            prices.append(value)
        if key == 'code':
            codes.append(value)

df = pd.DataFrame(list(zip(names, prices, codes)), columns=['Nazev', 'Cena', 'Kod'])

df.to_csv(r'Merkury_results.csv', index=False, sep=";")
