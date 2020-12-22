import json
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--mode', type=str, default='cz')
args = parser.parse_args()

with open('siko.json') as f:
    data = json.load(f)

with open('ean_to_url.json') as f:
    ean_to_url = json.load(f)

with open('siko_found_eans.txt') as f:
    found_eans = f.read().splitlines()

with open('siko_not_found_eans.txt') as f:
    not_found_eans = f.read().splitlines()

list_for_df = []
for i, entry in enumerate(data):
    ean = list(ean_to_url.keys())[list(ean_to_url.values()).index(entry['url'])]
    list_for_df.append([ean, entry['name'], entry['price']])

empty_names = ["ean nenalezen" for ean in not_found_eans]
empty_prices = ["" for ean in not_found_eans]

df_succes = pd.DataFrame(list_for_df, columns=['EAN', 'Nazev', 'Cena'])

df_fail = pd.DataFrame(list(zip(not_found_eans, empty_names, empty_prices)), columns =['EAN', 'Nazev', 'Cena'])

if args.mode == 'cz':
    df_succes.append(df_fail).to_csv(r'../../Scrape/output/SikoCZ_results.csv', index=False)
else:
    df_succes.append(df_fail).to_csv(r'../../Scrape/output/SikoSK_results.csv', index=False)
