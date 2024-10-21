import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

# This is a public url, containing Iranian national code identifiers (first three digits)
url = 'https://vakilazma.com/the-city-where-the-national-code-is-issued-with-the-first-three-digits/'

response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

data = {}
current_province = None

table = soup.find('table')
# print(table)

rows = table.find_all('tr')
# print(len(rows))

for row in rows:
    cols = row.find_all('td')
    if len(cols) == 2: 
        key = cols[0].text.strip()
        value = cols[1].text.strip()

        if "***" in key:
            current_province = value
            data[current_province] = [] 
        if current_province is not None:
            if '-' in key:
                parts = key.split('-')
                for part in parts:
                    data[current_province].append({part: value})
            else:
                data[current_province].append({key: value})

# To generate json file
# with open('data.json', 'w', encoding='utf-8') as json_file:
#     json.dump(data, json_file, ensure_ascii=False, indent=4)

# To generate excel file
rows_to_write = []
for province, cities in data.items():
    for city in cities:
        for code, name in city.items():
            rows_to_write.append([province, name, code])

df = pd.DataFrame(rows_to_write, columns=['Province', 'City', 'National Code'])

df.to_excel('data.xlsx', index=False, engine='openpyxl')
