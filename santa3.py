#!/usr/bin/python3.5

from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from threading import Thread
import os
import re
import socket
import requests
import queue
import time
import sys
import argparse
import datetime
from datetime import timedelta, date


def searchDate(daten, pattern):
    
    #main page
    urlBegin = "http://clerkrecorder.co.santa-cruz.ca.us/"
    phanthonPath = "/usr/bin/phantomjs"
    daten2 = daten.replace('/', '.')
    filename1 = "csv/" + daten2 + ".csv"
    
    txtDate = "[" + daten + "]:"
    print (txtDate, pattern, filename1)
        
    
    #field to save in cvs file
    docNumber = ""   
    yyyy = daten[6:]
    mm   = daten[:2]
    dd   = daten[3:5]
    recordDate = yyyy + "-" + mm + "-" + dd   
    docType = "docType"
    grantor = ""
    grantee = ""
    county = "santa-cruz"
    state = "CA"
     
    print (txtDate, "open main page ..")
    
    browser = webdriver.PhantomJS(phanthonPath)
    browser.get(urlBegin)
    #wait for load
    time.sleep(3)  
    soup1  = BeautifulSoup(browser.page_source, "html.parser")
    #print (soup1)
    #click on ack, si esta iendo a la segunbda pagina des pues de dar click en ack
    browser.find_element_by_id('cph1_lnkAccept').click()
    time.sleep(3)
    #print ("--------------------------------------------------------")
    soup1  = BeautifulSoup(browser.page_source, "html.parser")
    #print (soup1)
    
    #Click on menu 'Real Estate
    element = browser.find_element_by_link_text('Real Estate').click()
      
    time.sleep(2)
    #ver si hizo el roll over   
   
    soup1  = BeautifulSoup(browser.page_source, "html.parser")
    print ("------------------------despues del roll over--------------------------------")
    
    
    #click on Search state real index
    browser.find_element_by_id('x:273746300.10:adr:2.1').click()
    time.sleep(4)
    soup1  = BeautifulSoup(browser.page_source, "html.parser")
    print (soup1)
    browser.save_screenshot('screenie.png')
    #aqui me quede
    #quitar esto 
    return 
    
    
    
    #click  on button to start
    browser.find_element_by_class_name("productLink").click();
    
    #wait for load
    time.sleep(5)
   
    #select patter to search
    el = browser.find_element_by_id('vps:docType2')
    time.sleep(1)
    print ("Set pattern and date to search in main page..")
    for option in el.find_elements_by_tag_name('option'):
        
        if option.text == pattern:       
            option.click()
            break
        
   
    time.sleep(1)
    
    #set date to text field
    datetxt = browser.find_element_by_id("vps:beginDate2")
    datetxt.send_keys(daten) 
    
    time.sleep(3)
    
    #click on button search
    print ("Search records for date...", daten)
    browser.find_element_by_xpath("//*[@src ='/pc/images/search_v3.gif']").click()
    time.sleep(3)
    
    
    #open file to write results
    FILE1 = open(filename1, "w")
    cont  = 0
    print ("Proccess results...")
    #proccess current page, and click next button until complete it
    while True :
        
        #get current page
        soup5 = BeautifulSoup(browser.page_source, "html.parser")
        
        #search tables with results
        tables = soup5.findAll( "table", {"style":"margin:5px;"} )
        
        
        contTbl =1
        #proccess each table
        for table in tables:                 
            contTbl = contTbl + 1
            #proccess each row
            found = 0
            for row in table.findAll("tr"):
                
                #get all columns for this row
                cells = row.findAll("td")
                
                #get text from column and clean it
                cells =  [ele.text.strip() for ele in cells]
                
                               
                #this is the row for document
                if re.search('Document Number' ,cells[0] ) and len (cells) == 1 :                    
                    _, docNumber = cells[0].split(':')
                    docNumber = docNumber.replace(' ', '')                    
                #this is the row for grantor and grante
                if row.findAll("td", {"class" :"grantor_grantee"}) and len (cells) == 2 :                    
                    # I found what I need                    
                    found = 1
                    brs = row.findAll("br")                    
                    listGrantor =[]
                    listGrantee = []
                    f1 = 0
                    
                    for br in brs:
                        if str(br) == "<br/>" :
                            f1 = 1
                            continue
                        #remove invalid tags
                        txt = str(br)
                        txt = txt.replace("<br/>","")
                        txt = txt.replace("</br>","")
                        #split it
                        txt2 = txt.split ("<br>")
                        if f1 == 0 :                           
                           listGrantor= listGrantor + txt2
                        else :
                           listGrantee= listGrantee + txt2
                    
                    #remove spaces and empty strings
                    listGrantor = [i.strip() for i in listGrantor]
                    listGrantor = [j for j in listGrantor if len(j) > 1]
                    listGrantee = [i.strip() for i in listGrantee]
                    listGrantee = [j for j in listGrantee if len(j) > 1]
                    
                    #remove duplicate values
                    listGrantor2 = set(listGrantor)
                    listGrantee2 = set(listGrantee)
                    #print ("grantor", listGrantor2)
                    #print ("grantee", listGrantee2)
                    
            #write on file if i found what i need in this table
            if found == 1 :                
                #txt1 = docNumber + ","+ recordDate + "," + docType + "," + grantor + ","+ grantee + ","+county +"," + state +  "\n"
                txt1 = recordDate + "," + docNumber + ","+ docType + ","
                
                #grantor
                for grantor in listGrantor2:
                    txt2 = "Grantor" + "," + grantor + ",Unavailable," + county +"," + state + "\n"
                    txt3 = txt1 + txt2
                    FILE1.write(txt3)
                #grantee
                for grantee in listGrantee2:
                    txt2 = "Grantee" + "," + grantee + ",Unavailable," + county +"," + state + "\n"
                    txt3 = txt1 + txt2
                    FILE1.write(txt3)
               
            
        #break #to test first page
        #rewiew if next button exists on current page
        try :
            if browser.find_element_by_xpath("//*[@src ='/pc/images/nextPage_v3.gif']") :
                cont = cont + 1
        except (NoSuchElementException): # if not , break the loop
            break
        
        #ckick on next button
        browser.find_element_by_xpath("//*[@src ='/pc/images/nextPage_v3.gif']").click()
        time.sleep(2)
        print ("Results from page:", cont, "completed")
        
        
    #close driver and file    
    browser.quit()
    FILE1.close()
    
    
    print (txtDate,"completed")

def validateDate( date_text, formatn ):
    try:
        datetime.datetime.strptime(date_text, formatn)
    except ValueError:
        print("Incorrect data format for date ",date_text,"it should be " ,formatn )
        return -1
    else :
        return 1
    
def main():
    
    #prepare arguments to read
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--From', help='from date to search mmddyyyy', required=True)
    parser.add_argument('-t', '--To', help='To date to search mmddyyyy', required=True)
    parser.add_argument('-n', '--Number', help='n jobs to run simultaneous, e.i. 2 day n= 2, 3 days n = 3 ..', default = 1, type=int)
    args = parser.parse_args()
    
    maxTreats = args.Number    
    #validate dates
    if validateDate(args.From, "%m%d%Y" ) == -1 :
       return
    
    if validateDate(args.To, "%m%d%Y" ) == -1 :
       return
        
    #create range of dates
    end_date =   datetime.datetime.strptime(args.To, "%m%d%Y") 
    start_date = datetime.datetime.strptime(args.From, "%m%d%Y") 
    
    day_count = (end_date - start_date).days + 1
    #commands to run   
    Q1 = queue.Queue()
    daterange = []
    pattern = "DEED|DEED OF TRUST|RECONVEYANCE"
    for single_date in (start_date + timedelta(n) for n in range(day_count)):
        
        datetxt = single_date.strftime("%m/%d/%Y")
        
        #if csv file already exist for this day , omit it        
        dattmp = datetxt.replace('/', '.')
        filename2 = dattmp + ".csv"        
        filename2 = "csv/"+filename2        
        if os.path.isfile(filename2):
            print ("Report for day:", datetxt, " has been already ran, result is on file:",filename2)
            continue        
        daterange.append(datetxt)               
        Q1.put(datetxt)
        
    
    #run n jobs at the same time
    while not Q1.empty() :
          
        treats = []
        for i in range (maxTreats) :
            
            if Q1.empty() :
                break
            
            daten = Q1.get()
            print ("processing ... ", daten)
            t = Thread (target=searchDate, args=(daten, pattern) )       
    
            treats.append(t)
            t.start()
            
        for t1 in treats:
            t1.join()    
    
    print ("Process finished")
    

if __name__ == '__main__':
    
    main()
