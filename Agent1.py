#!/usr/bin/python3.4

"""set agent to simulate beeing human to scrap a site
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import socks
import socket
import ProxyLib
import requests


#proxy code is here

socket.socket  = ProxyLib.setLocalProxy(9050)
#socket.socket  = ProxyLib.setAnyProxy("187.161.162.253", 16492)
ProxyLib.printIp()

session = requests.Session()
#headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
#headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
url = "https://www.whatismybrowser.com/developers/what-http-headers-is-my-browser-sending"
req = session.get(url, headers=headers)
bsObj = BeautifulSoup(req.text)
print(bsObj.find("table",{"class":"table-striped"}).get_text)

exit (0)
