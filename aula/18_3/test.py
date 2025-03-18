#!/usr/bin/python3

import re
import shelve
import requests
from bs4 import BeautifulSoup as bs
from tabulate import tabulate

d = shelve.open('pagecache.db')

def myget(url):
    if url not in d:
        d[url] = requests.get(url).text
    return d[url]

url = 'https://www.jonsay.co.uk/dictionary.php?langa=Portuguese&langb=Chinese'
txt = myget(url)
dt = bs(txt, 'lxml')

d_pt_cn = []

for link in dt.find_all('a', class_='nav'):
    cat = link.text
    txt = myget(link['href'])
    dtf = bs(txt, 'lxml')

    for table in dtf.find_all('table', class_='mytable2'):
        for tr in table.find_all('tr'):
            children = tr.find_all('td')
            if len(children) == 3:
                pt,py,cn = children
                pt,py,cn = pt.text,py.text,cn.text
                d_pt_cn.append({'pt': pt, 'py': py, 'cn': cn, 'cat': cat})

print(tabulate(d_pt_cn))
