#!/usr/bin/python3.4

"""Get the Details of the competitor from this
http://www.alibris.com/

I am interested in finding out stores like this - http://www.alibris.com/stores/onestopm.

The details that are interesting to me on this page are the following:

Store name,
Seller since,
# of books for sale.

type: One Stop Music Shop

For this page, I have to set up the agent before requets it since it fails without do it
I got, soenitng like  'Connection reset by peer'
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import socks
import socket
import ProxyLib
import requests


#proxy code is here
#print current ip
#ProxyLib.printIp()
#socket.socket  = ProxyLib.setLocalProxy(9050)
socket.socket  = ProxyLib.setAnyProxy("187.161.162.253", 16492)
ProxyLib.printIp()

baseName = "http://www.alibris.com/findSeller?keyword="
def searchIt(nameCompetitor) :
    session = requests.Session()
    page1 = baseName + nameCompetitor
    print (page1)
   # html1  = urlopen(page1)
    #bsObj1 = BeautifulSoup(html1)
    #print (bsObj1)
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    req = session.get(page1, headers=headers)
    bsObj = BeautifulSoup(req.text)
    print(bsObj)

    ProxyLib.printIp()
    
inputTxt = ""
while inputTxt != "X" and inputTxt != "x" :
    inputTxt = input ("Enter competitor name ( x to finish):")
    #print (inputTxt)
    searchIt(inputTxt)
  
exit (0)  