#!/usr/bin/python3.4
from urllib.request import urlopen
from bs4 import BeautifulSoup

#read an html and use BeautifulSoup library to print in better format and try and catch statement

def getTitle(url):
    
    try:
        html = urlopen(url)
    except HTTPError as e:#invalid page
        return None
    
    try:
        bsObj = BeautifulSoup(html.read())
        title = bsObj.body.h1
    except AttributeError as e: #tag h1 does not exist
        return None
    
    return title


title = getTitle("http://www.pythonscraping.com/pages/page1.html")
if title == None:
    print("Title could not be found")
else:
    print(title)