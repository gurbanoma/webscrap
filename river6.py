#!/usr/bin/python3.5

from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import re
import socket
import requests
import ProxyLib
import time
import sys

#proxy code is here
#print current ip
#ProxyLib.printIp()
#socket.socket  = ProxyLib.setLocalProxy(9050)
#ProxyLib.printIp()



def searchDate(daten):
    urlBegin = "https://paymentsolutions.lexisnexis.com/pc/ca/co/riverside/officialrecords"
    #html = urlopen(urlBegin)
    #bsObj = BeautifulSoup(html.read())
    #print (bsObj)
    browser = webdriver.PhantomJS('/usr/bin/phantomjs')
    browser.get(urlBegin)
    soup  = BeautifulSoup(browser.page_source, "html.parser")
    
    print (soup)
    
    time.sleep(3)
    #forzar el click 
    browser.find_element_by_class_name("productLink").click();
    time.sleep(3)
    print ("---------------------------------------------------------------")
    #volver a leer el html 
    soup2  = BeautifulSoup(browser.page_source, "html.parser")
    #ahora ya tiene el nuevo contenido
    print (soup2)
    time.sleep(5)
    #move to seach
    print ("---------------search document------------------------------------------------")
    
    #select "DEED"
    el = browser.find_element_by_id('vps:docType2')
    time.sleep(1)
    for option in el.find_elements_by_tag_name('option'):
        #print (option.text)
        if option.text == 'DEED' :
            print (option.text)
            option.click()
            break
        
    #select.select_by_visible_text(....)
    time.sleep(1)
    
    #set text to date field
    datetxt = browser.find_element_by_id("vps:beginDate2")
    datetxt.send_keys(daten)
    time.sleep(1)
    soup3  = BeautifulSoup(browser.page_source, "html.parser")
    time.sleep(1)
    #ver si estan los valores recien cambiados
    print ("*****", browser.find_element_by_id("vps:beginDate2").get_attribute("value"))
    #selectItem.getFirstSelectedOption().getText();
    select = Select(browser.find_element_by_id('vps:docType2'))
    selected_option = select.first_selected_option
    print (selected_option.text)
    #print (soup3)
    print ("--------------hacer el query-------------------------")
    #set text
    time.sleep(3)
    #click sobre buscar y ya quedo
    browser.find_element_by_xpath("//*[@src ='/pc/images/search_v3.gif']").click()
    time.sleep(3)
    soup4  = BeautifulSoup(browser.page_source, "html.parser")
    print (soup4)
    #dar click en next unti nothing
    
    #ver su hay nex
    #if browser.find_element_by_xpath("//*[@src ='/pc/images/nextPage_v3.gif']") :
    #    print ( "***si hay next")
    
    cont  = 0
    #while browser.find_element_by_xpath("//*[@src ='/pc/images/nextPage_v3.gif']") :
    #      browser.find_element_by_xpath("//*[@src ='/pc/images/nextPage_v3.gif']").click()
    #      time.sleep(2)
    #      print (" pagina ", cont)
    #      cont = cont + 1
    while True :
        
        soup5 = BeautifulSoup(browser.page_source, "html.parser")
        tables = soup5.findAll( "table", {"style":"margin:5px;"} )
        
        print ("----------------------------------------tablas--------------------------------")
        contTbl =1
        for table in tables:
            print ("----->",contTbl )
           # print (table)
            contTbl = contTbl + 1
            #ir por los campos que me interesantes
            print ("-----rows----")
            for row in table.findAll("tr"):
                #print (row)
                
                cells = row.findAll("td")
                #obtener el texto de cada columan y meterlo a un arreglo
                cells =  [ele.text.strip() for ele in cells]
                #print(cells)
                
                #el row que tiene el doc
                if re.search('Document Number' ,cells[0] ) and len (cells) == 1 :
                    print(cells, "buenas 1 ")
                #es el que row de grantor_grantee
                if row.findAll("td", {"class" :"grantor_grantee"}) and len (cells) == 2 :
                    print(cells, "buenas 2")
           
            
        break
        #move to next page
        try :
            if browser.find_element_by_xpath("//*[@src ='/pc/images/nextPage_v3.gif']") :
                cont = cont + 1
        except (NoSuchElementException):
            break
        
        browser.find_element_by_xpath("//*[@src ='/pc/images/nextPage_v3.gif']").click()
        time.sleep(2)
        print (" pagina ", cont)
        
        if cont > 1 :
            break
        
    browser.quit()


def main():
    print ("hola mundo")
    #url = "https://paymentsolutions.lexisnexis.com/pc/ca/co/riverside/officialrecords"
    url = "https://paymentsolutions.lexisnexis.com/pc/pages/landing_page.xhtml"
    html = urlopen(url)
    daten = "12/31/2016"
    bsObj = BeautifulSoup(html.read())
    print (bsObj)
    #aqui me quede
    
if __name__ == '__main__':
    searchDate("12/30/2016")
