import pandas as pd
import json

main_link = 'https://www.baumax.cz/vyhledvn/szukaj.html?szukaj='

data = pd.read_csv('data.csv', sep=";")
data = data.loc[data['COUNTRY'] == 'CZ']
data = data.drop(data.loc[data['EAN'] == 0].index.values)
data_list = data['EAN'].to_list()
ean_list = data['EAN'].to_list()

data_dict = {}
for dat in zip(data_list, ean_list):
    data_dict[main_link + str(dat[0])] = str(dat[1])

with open('baumax_urls.json', 'w') as f:
    json.dump(data_dict, f)

#links = [main_link + str(code) for code in data_list]

#with open('baumax_urls.txt', 'w') as f:
#    for item in links:
#        f.write("%s\n" %item)
