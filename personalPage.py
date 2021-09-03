# Example： 從 Request 到 BeatifulSoup

import json
import requests
from bs4 import BeautifulSoup

url = 'https://scholar.google.com.tw/citations?user=g-_ZXGsAAAAJ&hl=zh-TW&oi=ao'
r = requests.get(url)
soup = BeautifulSoup(r.text)
'''
print(soup)
print(type(soup))
'''
# personal detail
info = {}

# id
content = ''.join(soup.find('meta', property='og:image')
                  ['content'])  # list to string
info['id'] = content.split('user=')[1].split('&citpid=1')[0]

d = soup.find('div', id='gsc_prf_i')

# name
info['name'] = d.find('div', id='gsc_prf_in').text

# university
info['university'] = d.find('a', class_='gsc_prf_ila').text

# email
email = d.find('div', id='gsc_prf_ivh').text.split(' ')[1]
info['email'] = email

# picture
info['picture'] = soup.find('div', id='gsc_prf_pua').find('img')['src']

label = []
for p in soup.find_all('a', class_='gsc_prf_inta gs_ibl'):

    label.append(p.text)
info['label'] = label
print(label)
'''print(info)'''

citeBy = {}
citations = {}
h_index = {}
i10_index = {}


def cited(status, value):

    if status / 2 < 1:
        if status % 2 == 0:
            citations['All'] = value
        else:
            citations['Since2016'] = value
        citeBy['citations'] = citations

    if status / 2 < 2:
        if status % 2 == 0:
            h_index['All'] = value
        else:
            h_index['Since2016'] = value
        citeBy['h_index'] = h_index

    if status / 2 < 3:
        if status % 2 == 0:
            i10_index['All'] = value
        else:
            i10_index['Since2016'] = value
        citeBy['i10_index'] = i10_index


count_d = 0
for d in soup.find_all('td', class_='gsc_rsb_std'):

    cited(count_d, d.text)

    count_d = count_d + 1

results = []

temp = {**info, **citeBy}
results.append(temp)


jsonStr = json.dumps(results)
print(jsonStr)

jsonFile = open("data.json", "w")
jsonFile.write(jsonStr)
jsonFile.close()
