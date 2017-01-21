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
    urlBegin = "http://publicrecords.countyofkings.com/"
    phanthonPath = "/usr/bin/phantomjs"
    daten2 = daten.replace('/', '.')
    filename1 = "csv/" + daten2 + ".csv"
    
    txtDate = "[" + daten + "]:"
    print (txtDate, "output file:",filename1)
        
    
    #field to save in cvs file
    docNumber = ""   
    yyyy = daten[6:]
    mm   = daten[:2]
    dd   = daten[3:5]
    recordDate = yyyy + "-" + mm + "-" + dd   
    docType = ""
    grantor = ""
    grantee = ""
    county = "kings"
    state = "CA"
    apnTxt   = "Unavailable"
     
    print (txtDate, "open main page ..")
    
    browser = webdriver.PhantomJS(phanthonPath)    
    browser.get(urlBegin)
    #wait for load
    time.sleep(3)  
    soup1  = BeautifulSoup(browser.page_source, "html.parser")
    
    #click on ack
    browser.find_element_by_id('cph1_lnkAccept').click()
    time.sleep(3)
    
    #Click on menu 'Real Estate
    element = browser.find_element_by_link_text('Real Estate').click()      
    time.sleep(2)
    
    #click on Search Real Estate Index after menu appear
    browser.find_element_by_id('x:273746300.43:adr:10.0').click()
    time.sleep(4)
    
    
    #input dates, from and to    
    datepicker = browser.find_element_by_id("x:2002578730.0:mkr:3")
    datepicker.click()
    datepicker.clear()   
    datepicker.send_keys(daten)
    time.sleep(1)
    
    datepicker2 = browser.find_element_by_id("x:625521537.0:mkr:3")
    datepicker2.click()
    datepicker2.clear()
    datepicker2.send_keys(daten)
    #datepicker2.send_keys("12/07/2016")
    time.sleep(1)
        
    #click en search   
    browser.find_element_by_id("cphNoMargin_SearchButtons2_btnSearch__3").click()   
    time.sleep(4)
           
    #create  csv file with header
    FILE1 = open(filename1, "w")
    FILE1.write("date,doc_number,document,role,name,apn,county,state\n")
        
    #get number of rows found from a span field
    rows = browser.find_element_by_id("cphNoMargin_cphNoMargin_SearchCriteriaTop_TotalRows")    
    nrow = int (rows.text)
    
    if  nrow <= 0 :
        print (txtDate,"nothing found for this date")    
        FILE1.close()
        return
    
    
    #move to the last page if that button is avialable, this is to know the total number of pages
    try :
        if browser.find_element_by_xpath("//*[@src ='/images/toolbaricons/lastpagesmall.gif']") :
            #move last page
            browser.find_element_by_xpath("//*[@src ='/images/toolbaricons/lastpagesmall.gif']").click()
            time.sleep(3)
            #browser.save_screenshot('lastPage.png')
    
            #back to first
            browser.find_element_by_xpath("//*[@src ='/images/toolbaricons/firstsmall.gif']").click()
            time.sleep(3)
            #browser.save_screenshot('FirstPage.png')
            
            
            
    except (NoSuchElementException) :
        pass
        
    count1 = 1
    
    #proccess current page, then click next
    while True :
                
        #get current page
        soup2 = BeautifulSoup(browser.page_source, "html.parser")       
        print (txtDate, "proccessing page:", count1)
           
        
        #find table
        table = soup2.find( "table", {"id":"x:1533160306.5:mkr:dataTbl.hdn"} )
        
        #get rows
        rows = table.findAll("tr")
        #####proccess each row
        apn   = "Unavailable"
        found = 0
        for row in rows:
            found  = 0
            #get columns
            cols = row.findAll("td")
            
            #get text of each column
            colc = [ele.text for ele in cols]            
            
            #not valid row
            if len ( colc) < 20 :
                continue
            docNumber = colc[3]
            docNumber = docNumber.strip()
            docType   = colc[8].strip()
                  
        
            #no valid document
            if  len(docNumber)< 1 :
                continue
                       
            #county
            apnTxt = ""
            if len (colc[17]) > 2 :
                apnTxt   = colc[17]
            else:
                apnTxt   = "Unavailable"
            
            
            #******consider all documents *****
            #only certain documents
            #if not re.search(pattern, docType) :
            #    continue
                        
            coln =str (row.find("td", {"class":" fauxDetailLink"}))
            coln = coln.replace('"', '')
            coln = coln.replace('<', '')
            coln = coln.replace('>', '')
            coln = coln.split(' ')
            
            idSearch = ""
            for item in coln :
                if re.search("id=", item) :
                   _ , idSearch = item.split("=")
            
            print (docNumber,docType, apnTxt)            
            print ("-->", idSearch)
            
            if len (idSearch) == 0 :
                continue
            
            #see details of this document
            browser.find_element_by_id(idSearch).click()
            time.sleep(2)
            tmpName = idSearch + ".png"
            
            #if count1 >= 13 :
            #   browser.save_screenshot(tmpName)
            browser.save_screenshot("id1.png")
            # ya entre al los detalles del primer row, aqui me quede quitar el return de aqui y el de 
            return            
            #search grantor
            listGrantor = []
            soup3 = BeautifulSoup(browser.page_source, "html.parser")
            table3 = soup3.find( "table", {"id":"ctl00_cphNoMargin_f_oprTab_tmpl0_DataList11"} )
            
            for row in table3.findAll("tr"):
                colgrantor = row.findAll("td")                
                colgrantor = [ c.text.strip() for c in colgrantor ]
                
                if len (colgrantor) < 4 :
                    continue
                if len (colgrantor[2])  == 0 :
                    continue
                
                grantortxt = colgrantor[2]
                
                grantortxt = grantortxt.replace('\t', '')
                grantortxt = grantortxt.replace('\n', '')
                
                if len (grantortxt) > 0:
                    listGrantor.append(str(grantortxt))
                    found = 1
            
            #search grantee
            listGrantee = []
            table4 = soup3.find( "table", {"id":"ctl00_cphNoMargin_f_oprTab_tmpl0_Datalist1"} )
            
            for row in table4.findAll("tr"):
                colgrantee = row.findAll("td")                
                colgrantee = [ c.text.strip() for c in colgrantee ]
                if len (colgrantee) < 4 :
                    continue
                if len (colgrantee[2])  == 0 :
                    continue
                
                granteetxt = colgrantee[2]
                
                granteetxt = granteetxt.replace('\t', '')
                granteetxt = granteetxt.replace('\n', '')
                
                if len (granteetxt) > 0:
                    listGrantee.append(str(granteetxt))
                    found = 1
            ###print on cvs files
            if found == 1 :                                
                txt1 = recordDate + "," + docNumber + ","+ docType + ","
                
                #grantor
                for grantor in listGrantor:
                    txt2 = "Grantor" + "," + grantor + "," + apnTxt +  "," + county +"," + state + "\n"
                    txt3 = txt1 + txt2
                    FILE1.write(txt3)
                #grantee
                for grantee in listGrantee:
                    txt2 = "Grantee" + "," + grantee +  "," + apnTxt +  "," + county +"," + state + "\n"
                    txt3 = txt1 + txt2
                    FILE1.write(txt3)
            #back to page
           
            browser.back()
            time.sleep(1)
            
            
        ###end of all rows
        
        break #only for test firts page
       
        #move to next page        
        try :
           if browser.find_element_by_xpath("//*[@src ='/images/toolbaricons/nextsmall.gif']") :
              pass
        except (NoSuchElementException) :# in last page , next button does not exist            
            break 
        
        browser.find_element_by_xpath("//*[@src ='/images/toolbaricons/nextsmall.gif']").click()
        time.sleep(2)
        count1 += 1
    ##end of all pages    
    
    FILE1.close()
    browser.quit()    
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
    pattern = "^(DEED|DEED OF TRUST|RECONVEYANCE)$"
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
