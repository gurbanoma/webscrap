#!/usr/bin/python3.4

"""makeProxy.py: como usar un proxy en python
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import socks
import socket

#aqui digo que mi proxy es mi local host, por el puerto 9050, pero como en
#el 9050 esta corriendo el tor esconde mi ip
socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)

#En http://proxylist.hidemyass.com/search-1664132#listable me encontre este proxy y si funciona muy bien
#aunque tardo mucho en connectarse pero muy bien funciona
#socks.set_default_proxy(socks.SOCKS5, "187.161.162.253", 16492)

#supongo que aqui prende el proxy
socket.socket = socks.socksocket
#en esta pagina solo muestra mi ip, para porbar ,abre la pagina y luego corre el scrip
#y veras dos ip diferentes
print(urlopen('http://icanhazip.com').read())

exit (0)
