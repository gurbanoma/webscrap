#!/usr/bin/python3.4

"""Get the Details of the competitor from this
http://www.alibris.com/

I am interested in finding out stores like this - http://www.alibris.com/stores/onestopm.

The details that are interesting to me on this page are the following:

Store name,
Seller since,
# of books for sale.
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

baseName = "http://www.alibris.com/findSeller?keyword="
def searchIt(nameCompetitor) :
    page1 = baseName + nameCompetitor
    print (page1)
    html1  = urlopen(page1)
    bsObj1 = BeautifulSoup(html1)
    print (bsObj1)
    
inputTxt = ""
while inputTxt != "X" and inputTxt != "x" :
    inputTxt = input ("Enter competitor name ( x to finish):")
    #print (inputTxt)
    searchIt(inputTxt)
  
exit (0)  
