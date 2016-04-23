#!/usr/bin/python3.4

"""HolidayDays.py: script to get holidays from 2000 t0 2016 in this page
http://www.timeanddate.com/calendar/?year=2016&country=1
Holiday are in the US
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

y = 2000
while y < 2017 :

 page = "http://www.timeanddate.com/calendar/?year=" + str(y) + "&country=1"
 #html = urlopen("http://www.timeanddate.com/calendar/?year=2016&country=1")
 html = urlopen(page)
 bsObj = BeautifulSoup(html)

 #search this table which contain the holidays
 table = bsObj.find("table", { "id" : "ch1" })

 #inside the table, we have 3 tables, each one in each column of the parent table

 print  ( "Holidays in " + str(y))
 for row in table.findAll("table", {"class": "cht lpad"}) :

    #get only the rows of the table
    #here is one sample of a row
    #<tr><td><span class="co1">Jan 1</span></td><td><a href="/holidays/us/new-year-day" title="New Year&#39;s Day is the first day of the Gregorian calendar, which is widely used in many countries such as the USA. ">New Year&#39;s Day</a></td></tr>
    for row2 in row.findAll("tr"):
        #get the text of the first column, which is the day       
        dia = row2.td.get_text()
        
        #get all the content of the firts column   
        tipo = row2.td
        #split to see if we have class="col"  this is a holiday , example = <td><span class="co1">Jan 1</span>...
        tipo2 = str(tipo).split("=")
        #get text of the second column which is the description day
        texto = row2.td.next_sibling.get_text()
        
        #if we have class= then   it is a holiday
        if ( len(tipo2) > 1) :
            print (dia + "," +texto)
        
 #next year
 y += 1