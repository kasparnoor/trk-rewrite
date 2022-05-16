from csv import excel
import requests
from bs4 import BeautifulSoup
import os 
import requests_cache
from . import app_config

requests_cache.install_cache(cache_name='geturls_cache', backend='sqlite', expire_after=180)

def geturls():
    
    # Making the request to the URL of starting times
    page = requests.get(app_config.classes_url)

    data = []
    # Parsing the HTML with beautifulsoup
    soup = BeautifulSoup(page.content, "html.parser")
    # Finding the correct table (there are two tables in the entire html document, one with the school title and second with the actual classes info)
    classes_table = soup.find("table", {"cellspacing" : "1"})
    # Get the data cells (from now on let's call them rows) from the found table
    classes_table_rows = classes_table.findAll("td")
    # Creating the list for the classes from the html
    raw_classes = []
    # Adding the classes to the list
    for index, item in enumerate(classes_table_rows):
        raw_classes.append(classes_table_rows[index])
    # Cleaning up the classes
    cleaned_classes = []
    for item in raw_classes:
        try:
            html_name = str(item).split("href=\"")[1].split("\"")[0]
        except:
            continue;
        html_url = app_config.classes_url.split("/d")[0] + "/" + html_name
        class_name = html_name.split("_")[1].split(".")[0]
        cleaned_classes.append([class_name, html_url])
    if app_config.conf_app_debug == 'true':
        print(cleaned_classes)
    return(cleaned_classes)