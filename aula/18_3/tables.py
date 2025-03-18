#!/usr/bin/python3
import re, csv
import shelve
import requests
from bs4 import BeautifulSoup as bs
import jjcli
from tabulate import tabulate

d = shelve.open("pagecache.db")
def my_get(url):
    if url not in d:
        print(f"...Geting {url}...")
        d[url] = requests.get(url).text
    return d[url] 

d_pt_py_cn = []

def main():
    cl = jjcli.clfilter("s:")
    sep = cl.opt.get("-s", " :: ")
    
    for url in cl.args:
        txt = my_get(url)
        dts = bs(txt,'lxml')
        for table in dts.find_all("table"):
            n = 1
            output = ""q
            
            if table.find_all("table"): continue
            
            for tr in table.find_all("tr"):
                children = [re.sub(r"\s+"," ", child.text) for child in tr.find_all("td")]
                output += sep.join(children) + "\n"
            
            print(f"==> {url}//{n}\n{output}")
            
main()
print(tabulate(d_pt_py_cn))
d.close()

