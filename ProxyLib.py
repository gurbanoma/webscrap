#!/usr/bin/python3.4

"""makeProxy.py: proxy libraries
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import socks
import socket


#run first
def printIp() :
    print(urlopen('http://icanhazip.com').read())
    
def setLocalProxy( port = 9050):
    """
    Hide my current ip, run first in linux tor service before call it (sudo /etc/init.d/tor start)
    param : port   9050 is the port of tor, run to get it (ss -aln | grep 9050)
    """
    socks.set_default_proxy(socks.SOCKS5, "localhost", port)
    
    return socks.socksocket
def setAnyProxy (ip, *others) :
    """
    set a proxy
    param : ip , port, user, password, flags           
    """
    if len (others) == 1 :
        port = others[0]
        socks.set_default_proxy(socks.SOCKS5, ip, port)
    #add more options when password and user are required
    else :
        socks.set_default_proxy(socks.SOCKS5, ip)
    
    return socks.socksocket
    
    
    
def main():
    #print current ip
    print ("My current ip is")
    print(urlopen('http://icanhazip.com').read())    
    #set proxy
    socks.set_default_proxy(socks.SOCKS5, "187.161.162.253", 16492)
    socket.socket = socks.socksocket
    print ("My new Ip after using a proxy")
    print(urlopen('http://icanhazip.com').read()) 
    

if __name__ == '__main__':
    main()
    exit (0)