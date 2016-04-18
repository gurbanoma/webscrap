#!/usr/bin/python3.4
from urllib.request import urlopen
from bs4 import BeautifulSoup

#read an html and use BeautifulSoup and get CSS
html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bsObj = BeautifulSoup(html)

#get the text that used css class green
nameList = bsObj.findAll("span", {"class":"green"})
for name in nameList:
    print(name.get_text())