from csv import excel
import requests
from bs4 import BeautifulSoup
import os 
import requests_cache
from . import app_config

requests_cache.install_cache(cache_name='getmultipletimes_cache', backend='sqlite', expire_after=180)

def getmultipletimes(target):
    
    # Making the request to the URL of starting times
    page = requests.get(app_config.timetable_url)

    # Parsing the HTML with beautifulsoup
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Finding all tables with info
    tables = soup.findAll("div", {"class":"accordion__content"})[2:]
    if target < 5 or target > 12:
        return("Invalid target")
    index = target - 5
    return(tables[index].find('tbody'))