from unittest import skip
import requests
from bs4 import BeautifulSoup
import datetime
import os 
import requests_cache
from . import app_config
from . import getmultipletimes

requests_cache.install_cache(cache_name='gettimesraw_cache', backend='sqlite', expire_after=180)
def gettimesraw(target):
    
    klass_table_body = getmultipletimes.getmultipletimes(target)
    data = []
    # Getting the rows in the table of 8kl body
    rows = klass_table_body.find_all('tr')
    # Getting the columns, part of parsing the table, somehow made it work
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    # Creating the table for times
    times = []
    # Checking every row in previously parsed columns

    for row in data:
        # Removing eating breakes from the list
        if "söög" in row[0]:
            data.remove(row)
            break;
    for row in data:
        # Formatting the time a bit
        index = row[0][0]
        time = row[1].split('-')[0]
        time = row[1].split('–')[0]
        times.append(time)

    return(times)