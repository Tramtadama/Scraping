import json
import pandas as pd

with open('baumax_products.json') as f:
    products = json.load(f)

with open('baumax_urls.json') as f:
    urls = json.load(f)

with open('products.json') as f:
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
        if key == 'ean':
            eans.append(value)

data = pd.read_csv('data.csv', sep=";")
data = data.loc[data['COUNTRY'] == 'CZ']
ean_list = data['EAN'].to_list()

ean_list = [str(ean) for ean in ean_list]
eans = [str(ean) for ean in eans]

missing_eans = list(set(ean_list) - set(eans))
print(len(missing_eans))

empty_names = []
empty_prices = []
empty_codes = []
for ean in missing_eans:
    empty_names.append("Produkt nenalezen")
    empty_prices.append("")
    empty_codes.append("")

empty_df = pd.DataFrame(list(zip(missing_eans, empty_names, empty_prices, empty_codes)),
        columns=['EAN', 'Nazev', 'Cena', 'Kod'])

df = pd.DataFrame(list(zip(eans, names, prices, codes)), columns=['EAN',
    'Nazev', 'Cena', 'Kod'])

df.append(empty_df).to_csv(r'Baumax_results.csv', index=False, sep=";")
