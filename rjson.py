#!/usr/bin/python3.4
from urllib.request import urlopen
import json

#this json works 
def getCountry():
    response = urlopen("https://maps.googleapis.com/maps/api/geocode/json?address=1+Science+Park+Boston+MA+02114&key=AIzaSyC0_rHfJptYpZLk65-5SBEPXM5_fBTS0fk").read().decode('utf-8')
    responseJson = json.loads(response)
    return responseJson.get("results")
    #return ""

print(getCountry())