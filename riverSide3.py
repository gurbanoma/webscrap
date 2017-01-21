#!/usr/bin/python3.5

from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from threading import Thread
import os
import re
import socket
import requests
import time
import sys
import argparse
import datetime
from datetime import timedelta, date



def searchDate(daten, pattern):
    
    #main page
    urlBegin = "https://paymentsolutions.lexisnexis.com/pc/ca/co/riverside/officialrecords"
    phanthonPath = "/usr/bin/phantomjs"
    pattern2 = pattern.replace(' ', '')
    daten2 = daten.replace('/', '')
    filename1 = pattern2 + "_" + daten2 + ".txt"
    filename2 = filename1 + "_completed"
    
    #check if this pattern has been completed for this date    
    if os.path.isfile(filename2):
        print ("Pattern:", pattern,"has been proccesed for date:",daten,"result is on file:",filename2)
        return
    
    
        
    #field to save in cvs file
    docNumber = ""
    recordDate = daten
    docType = pattern
    grantor = ""
    grantee = ""
    county = "Riverside"
    state = "CA"
     
    print ("Open main page to search", pattern , "for date", daten)
    browser = webdriver.PhantomJS(phanthonPath)
    browser.get(urlBegin)
    
    #wait for load
    time.sleep(3)
    
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
    
    #change file name to completed
    os.rename(filename1,filename2)
    print ("completed for date:",daten, "pattern:",pattern )

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
    parser.add_argument('-n', '--Number', help='n jobs to run simultaneous', default = 1, type=int)
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
    commands = []
    daterange = []
    for single_date in (start_date + timedelta(n) for n in range(day_count)):
        
        datetxt = single_date.strftime("%m/%d/%Y")
        daterange.append(datetxt)
        t1 = (datetxt, "DEED")
        t2 = (datetxt, "DEED OF TRUST")
        t3 = (datetxt, "RECONVEYANCE")
        commands.append(t1)
        commands.append(t2)
        commands.append(t3)
    
    
   
    #run multitread if client sent  n jobs
    countTreats  = 1
    treats = []
    for daten, pattern in commands:
        
        if countTreats < maxTreats : #threat it
            t = Thread (target=searchDate, args=(daten,pattern,) )
            treats.append(t)
            t.start()
        else :
            searchDate(daten,pattern )
        
        countTreats = countTreats + 1
    
            
    #wait for all threats, if any
    for t1 in treats:
        t1.join() 
    
    #mergue files to creat only 1 per day
    
    for d1 in daterange:
        dattmp = d1.replace('/', '')
        filesp = []
        
        filename1 = "DEED_" + dattmp + ".txt_completed"        
        if os.path.isfile(filename1):            
            filesp.append(filename1)
            
        filename1 = "DEEDOFTRUST_" + dattmp + ".txt_completed"        
        if os.path.isfile(filename1):            
            filesp.append(filename1)
        
        filename1 = "RECONVEYANCE_" + dattmp + ".txt_completed"        
        if os.path.isfile(filename1):           
            filesp.append(filename1)
        
        #create the new one for this day
        dattmp = d1.replace('/', '.')
        filename1 = dattmp + ".csv"
        
        #write headers
        FILE2 = open(filename1, "w")
        FILE2.write("date,doc_number,document,role,name,apn,county,state\n")
        FILE2.close()
        time.sleep(1)
        
        #append content to csv file
        with open(filename1, 'a') as outfile:
            for fname in filesp:
                with open(fname) as infile:
                     outfile.write(infile.read())
        print ("Report completed for day:",d1, "result is in file:",filename1 )
        
        #delete *completed files
        for fname in filesp:
            os.remove(fname)
if __name__ == '__main__':
    
    main()
