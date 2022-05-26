import enum
from itertools import count
import requests
from bs4 import BeautifulSoup
from . import geturls
import requests_cache
from . import app_config
requests_cache.install_cache(cache_name='getlessons_cache', backend='sqlite', expire_after=180)

def divide_chunks(l, n):
      
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

def getlessons(target):
    search_string = target
    for class_and_url in geturls.geturls():
        if search_string in class_and_url[0]:
            URL = class_and_url[1]
            break;
    page = requests.get(URL)

    data = []
    soup = BeautifulSoup(page.content, "html.parser")

    kaheksasklass_table = soup.find("table", {"border" : "3"})
    kaheksasklass_table_rows = kaheksasklass_table.findAll("tr")
    kaheksasklass_table_days = kaheksasklass_table_rows[0]
    kaheksasklass_table_tables = kaheksasklass_table.findAll("table")

    raw_lessons = []

    del kaheksasklass_table_tables[0:6]

    for index, item in enumerate(kaheksasklass_table_tables):
        raw_lessons.append(kaheksasklass_table_tables[index])
        

    processed_lessons = list()
    for lesson in raw_lessons:
        if raw_lessons.index(lesson) in [0, 6, 12, 18, 24, 30, 36, 42, 48, 54]:
            continue
        raw_info = lesson.find_all("font")
        if raw_info:
            processed_info = []
            if len(raw_info) == 3:
                for info in raw_info:
                    info_text = info.text.strip()
                    processed_info.append(info_text)
                processed_lessons.append([processed_info])
            elif len(raw_info) == 6:
                first_lesson_info = []
                second_lesson_info = []
                double_lesson_info = []
                for i in [0,1,2]:
                    info = raw_info[i]
                    info_text = info.text.strip()
                    first_lesson_info.append(info_text)
                double_lesson_info.append(first_lesson_info)
                for i in [3,4,5]:
                    info = raw_info[i]
                    info_text = info.text.strip()
                    second_lesson_info.append(info_text)
                double_lesson_info.append(second_lesson_info)
                processed_lessons.append(double_lesson_info)
            elif len(raw_info) == 9:
                first_lesson_info = []
                second_lesson_info = []
                third_lesson_info = []
                triple_lesson_info = []
                for i in [0,1,2]:
                    info = raw_info[i]
                    info_text = info.text.strip()
                    first_lesson_info.append(info_text)
                triple_lesson_info.append(first_lesson_info)
                for i in [3,4,5]:
                    info = raw_info[i]
                    info_text = info.text.strip()
                    second_lesson_info.append(info_text)
                triple_lesson_info.append(second_lesson_info)
                for i in [6,7,8]:
                    info = raw_info[i]
                    info_text = info.text.strip()
                    third_lesson_info.append(info_text)
                triple_lesson_info.append(third_lesson_info)
                processed_lessons.append(triple_lesson_info)
            elif len(raw_info) == 4:
                raw_info.insert(1, " ")
                raw_info.insert(4, " ")
                first_lesson_info = []
                second_lesson_info = []
                double_lesson_info = []
                for i in [0,1,2]:
                    info = raw_info[i]
                    try:
                        info_text = info.text.strip()
                    except:
                        if app_config.conf_app_debug == 'true':
                            print("Error line 97 getlessons.py")                            
                    first_lesson_info.append(info_text)
                double_lesson_info.append(first_lesson_info)
                for i in [3,4,5]:
                    info = raw_info[i]
                    try:
                        info_text = info.text.strip()
                    except:
                        if app_config.conf_app_debug == 'true':
                            print("Error line 106 getlessons.py")           
                    second_lesson_info.append(info_text)
                double_lesson_info.append(second_lesson_info)
                processed_lessons.append(double_lesson_info)
            else:
                for info in raw_info:
                    info_text = info.text.strip()
                    processed_info.append(info_text)
                processed_lessons.append(processed_info)
        else:
            empty = []
            processed_lessons.append(empty)

    # processed_lessons = list(divide_chunks(processed_lessons, 5))

    return(processed_lessons)
    #print(kaheksasklass_table_tables[23])

    # kaheksasklass_table_tables[0] - 1
    # kaheksasklass_table_tables[6] - 2
    # kaheksasklass_table_tables[12] - 3
    # kaheksasklass_table_tables[18] - 4
    # kaheksasklass_table_tables[24] - 5
    # kaheksasklass_table_tables[30] - 6
    # kaheksasklass_table_tables[36] - 7
    # kaheksasklass_table_tables[42] - 8
    # kaheksasklass_table_tables[48] - 9
    # kaheksasklass_table_tables[54] - 10