#!/usr/bin/python3.4
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

#get entire site 
pages = set()

def getLinks(articleUrl) :
    global pages
    #read an html and use BeautifulSoup and get CSS
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html)
    try :
        print(bsObj.h1.get_text())
        print(bsObj.find(id ="mw-content-text").findAll("p")[0])
        print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href'])
    except AttributeError:
        print("This page is missing something! No worries though!")
        
    for link in bsObj.findAll("a",href=re.compile("^(/wiki/)")) :
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages :
                newpage = link.attrs['href']
                print("----------------\n" + newpage)               
                pages.add(newpage)
                getLinks(newpage)


getLinks("")

        
