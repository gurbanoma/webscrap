#!/usr/bin/python3.4
from urllib.request import urlopen

#read an html an print it in the terminal
html = urlopen("http://pythonscraping.com/pages/page1.html")
print(html.read())
