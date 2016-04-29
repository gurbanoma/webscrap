#!/usr/bin/python3.4

"""Get the Details of each program, we have 2931 founds here
http://tools.canlearn.ca/cslgs-scpse/cln-cln/rep-fit/p/af.p.clres.do?institution_id=default&searchType=ALL&searchString=&progLang=A&instType=B&prov_1=prov_1&progNameOnly=N&start=0&finish=19&section=1
so, I open each number of pages  and in each page I get the link of the program and open the page, here is one sample of the page

http://tools.canlearn.ca/cslgs-scpse/cln-cln/rep-fit/p/af.p.cldet.do?institution_id=default&amp;searchType=ALL&amp;searchString=&amp;progLang=A&amp;instType=B&amp;prov_1=prov_1&amp;progNameOnly=N&amp;start=0&amp;finish=19&amp;section=1&pro=6683&details=general

in the final link, get the datails which are in the div and that's it
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

ini2 = 0
fin2 = 19
base1 = "http://tools.canlearn.ca/cslgs-scpse/cln-cln/rep-fit/p/"
pages = []

#open 20 founds by 20 founds
while fin2 <= 2931 :
    
    #page1 = "http://tools.canlearn.ca/cslgs-scpse/cln-cln/rep-fit/p/af.p.clres.do?institution_id=default&searchType=ALL&searchString=&progLang=A&instType=B&prov_1=prov_1&progNameOnly=N&start=0&finish=19&section=1"
    page1 = "http://tools.canlearn.ca/cslgs-scpse/cln-cln/rep-fit/p/af.p.clres.do?institution_id=default&searchType=ALL&searchString=&progLang=A&instType=B&prov_1=prov_1&progNameOnly=N&start="+ str(ini2)+"&finish="+str(fin2)+"&section=1"
    html1  = urlopen(page1)
    bsObj1 = BeautifulSoup(html1)
    
    #get the 20 links of this page and save it
    for links in bsObj1.findAll("strong") :
        txt1 = str(links)
        ini = txt1.find("href=")
        end = txt1.find("details=general")
        if ini != -1 and end != -1 :
            ini += 6
            end += 15
            txt2 = txt1[ini:end]
            txt2 = txt2.replace(';amp', '')
            txt2 = txt2.replace('&amp;pro=', '&pro=')
            txt2 = txt2.replace('&amp;details=', '&details=')
    
            pages.append(txt2)   
    ini2 += 20
    fin2 += 20

#open each link and get the details of this program
for p1 in pages:
    html2 = base1 + p1
    
    

    html = urlopen(html2)
    bsObj = BeautifulSoup(html)

     #search this table which contain the holidays
    form1 = bsObj.find("h2", {"id" :"programName"})
    text1 = form1.get_text()

    text1 = text1.replace('\n', ' ')
    text1 = text1.replace('\r', ' ')
    text1 = text1.replace('  ', '')

    print (text1)

    #get details of this program like this
    #Advanced Massage Therapy Diploma - Part-time Alberta Institute of Massage
    #Program Level: College or CEGEP postsecondary program 
    #Credential Type: Diploma 
    #Joint Program Level: Not entered 
    #Joint Credential Type: Not entered 
    #Address: Alberta Institute of Massage7710 Gaetz Avenue Red Deer , Alberta T4P 2A5Canada 
    #Telephone: (403) 346-1018
    #Fax: (403) 346-0606
    #Email: info@AlbertaInstituteOfMassage.com 
    flag1 = 0
    for div1 in bsObj.findAll("div", {"class": "grid-12 equalize cl-border-top-dot"}) :
        
        txt1 = div1.get_text()
        txt1 = txt1.replace('\n', ' ')
        txt1 = txt1.replace('\r', ' ')
        txt1 = txt1.replace('  ', '')
    
        if flag1 == 0 :
            if re.match(".*Program Level.*",txt1) :
                flag1 = 1
            
        if flag1 == 1 :
            print (txt1)
          
        
        