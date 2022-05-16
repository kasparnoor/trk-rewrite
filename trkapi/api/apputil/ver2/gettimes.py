from unittest import skip
import requests
from bs4 import BeautifulSoup
import datetime
import os 
import requests_cache
from . import app_config
from . import getmultipletimes

requests_cache.install_cache(cache_name='gettimes_cache', backend='sqlite', expire_after=180)
def gettimes(target):
    
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
    # Parsing the time "strings" as actual datetimes
    for time in times:
        newtime = time.replace(".", ":")
        newtime2 = datetime.datetime.strptime(newtime, "%H:%M")
        now = datetime.datetime.now()
        newtime3 = newtime2.replace(now.year, now.month, now.day)
        if app_config.conf_app_date_simulation == "true":
            newtime3 = newtime2.replace(int(app_config.conf_app_simulation_date.split(", ")[0]), int(app_config.conf_app_simulation_date.split(", ")[1]), int(app_config.conf_app_simulation_date.split(", ")[2]))
        times[times.index(time)] = newtime3

    return(times)