import requests
from bs4 import BeautifulSoup
import datetime


def getCurrentTime():
    now = datetime.datetime.now()
    currentTime = now.strftime("%Y-%m-%d %H:%M:%S")
    return currentTime

# personal detail


# personal detail
def getPersonalData(soup):
    info = {}
    d = soup.find('div', id='gsc_prf_i')

    # name
    info['name'] = d.find('div', id='gsc_prf_in').text
    # university
    try:
        info['university'] = d.find('a', class_='gsc_prf_ila').text
    except:
        info['university'] = ' '
    # picture
    info['picture'] = soup.find('div', id='gsc_prf_pua').find('img')['src']

    label = []
    for p in soup.find_all('a', class_='gsc_prf_inta gs_ibl'):

        label.append(p.text)
    info['label'] = label
    info['updateTime'] = getCurrentTime()
    return info


def getCiteBy(soup):
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

    return citeBy


def result(soup, ID):
    infos = {}
    infos['id'] = ID
    infos['personalData'] = getPersonalData(soup)
    infos['cited'] = getCiteBy(soup)

    return infos


def getPersonalPage(id):
    url = 'https://scholar.google.com.tw/citations?hl=zh-TW&user=' + id
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    return result(soup, id)
