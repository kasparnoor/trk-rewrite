from . import gettimes
from . import getlessons
from . import gettimesraw

import datetime
from datetime import timedelta
import requests_cache
from . import app_config
from itertools import chain
requests_cache.install_cache(cache_name='getnextlesson_cache', backend='sqlite', expire_after=180)
def getnextlesson(target):
    
    now = datetime.datetime.now()
    day = now.strftime("%A")
    time = now.time()

    times = gettimes.gettimes(int(list(target)[0]))
    lessons = getlessons.getlessons(target)

    lessons_1 = lessons[::5]
    lessons_2 = lessons[1::5]
    lessons_3 = lessons[2::5]
    lessons_4 = lessons[3::5]
    lessons_5 = lessons[4::5]

    if app_config.conf_app_date_simulation == "true":
        currenttime = datetime.datetime(int(app_config.conf_app_simulation_date.split(", ")[0]), int(app_config.conf_app_simulation_date.split(", ")[1]), int(app_config.conf_app_simulation_date.split(", ")[2]), int(app_config.conf_app_simulation_date.split(", ")[3]), int(app_config.conf_app_simulation_date.split(", ")[4]))
    else:
        currenttime = datetime.datetime.now()
        

    today = str(currenttime.weekday() + 1)
    lessons_ = "lessons_"
    today_lessons = lessons_ + today
    if today_lessons in "lessons_6" or today_lessons in "lessons_7":
        return
    today_lessons = locals()[today_lessons]
    for time in times:
        lesson_end = time + timedelta(minutes=45)
        # Lesson is ongoing
        if currenttime.time() > time.time() and currenttime.time() < lesson_end.time():
            time_until_lesson_end = lesson_end - currenttime
            lessons_remaining = today_lessons
            lessons_remaining = lessons_remaining[times.index(time)+1:]
            new_lessons_remaining = []
            for index, lesson in enumerate(lessons_remaining):
                try:
                    new_lessons_remaining.append([times[times.index(time) + index + 1],lesson])
                except:
                    if 0 == 1 : print("hi")
            
            info = [["ending", today_lessons[times.index(time)], time_until_lesson_end.total_seconds()],new_lessons_remaining]
            print(info)             
            return(info)
        # Time until next lesson
        if currenttime.time() < time.time() and currenttime.time() < lesson_end.time():
            next_lesson = times[times.index(time)]
            time_until_next_lesson = next_lesson - currenttime
            
            lessons_remaining = today_lessons
            lessons_remaining = lessons_remaining[times.index(time)+1:]
            new_lessons_remaining = []
            for index, lesson in enumerate(lessons_remaining):
                try:
                    new_lessons_remaining.append([times[times.index(time) + index + 1],lesson])
                except:
                    if 0 == 1 : print("hi")
            
            info = [["starting", today_lessons[times.index(time)], time_until_next_lesson.total_seconds()],new_lessons_remaining]
            print(info)            
            return(info)

getnextlesson("8C")
