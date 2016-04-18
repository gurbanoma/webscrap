#!/usr/bin/python3.4
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
#read an html and use BeautifulSoup and get CSS
html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html)

#read all url from wikipedia article

for link in bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
#for link in bsObj.findAll('a') :
    if 'href' in link.attrs:
        print(link.attrs['href'])
        
