import pandas as pd
import json

main_link = 'https://www.merkurymarket.sk/wyszukiwarka/szukaj.html?szukaj='

data = pd.read_csv('baumax_results.csv', sep=";").dropna()
ean_list = data['EAN'].to_list()
code_list = data['Kod'].to_list()

data_dict = {}

for dat in zip(code_list, ean_list):
    data_dict[main_link + str(int(dat[0]))] = str(dat[1])

with open('merkury_urls.json', 'w') as f:
    json.dump(data_dict, f)
