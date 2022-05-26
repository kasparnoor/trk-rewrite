from . import gettimes
from . import getlessons
from . import gettimesraw

import datetime
from datetime import timedelta
import requests_cache
from . import app_config
from itertools import chain
requests_cache.install_cache(
    cache_name='getnextlesson_cache', backend='sqlite', expire_after=180)


def getnextlesson(target):

    # Get current time
    now = datetime.datetime.now()
    day = now.strftime("%A")
    time = now.time()

    # Get lesson times by using the gettimes function, passing in the class name of which the information is needed about.
    # This allows us to know when all the lessons start.
    # It returns a list of datetimes that look like this datetime.datetime(2022, 5, 16, 8, 10)
    times = gettimes.gettimes(int(list(target)[0]))

    # Get list of all lessons by using the getlessons function, passing in the target class once again
    # Returns a list of lists that contain information about the lessons such as the lesson name, teacher and room
    lessons = getlessons.getlessons(target)

    # We’re using list slicing to create five separate lists of lessons.
    lessons_1 = lessons[::5]  # Get every lesson of monday
    lessons_2 = lessons[1::5]  # Get every lesson of tuesday
    lessons_3 = lessons[2::5]  # Get every lesson of wednesday
    lessons_4 = lessons[3::5]  # Get every lesson of thursday
    lessons_5 = lessons[4::5]  # Get every lesson of friday

    # If date simulation is enabled in the app config, then change currenttime to the date specified in the config
    if app_config.conf_app_date_simulation == "true":
        currenttime = datetime.datetime(int(app_config.conf_app_simulation_date.split(", ")[0]), int(app_config.conf_app_simulation_date.split(", ")[1]), int(
            app_config.conf_app_simulation_date.split(", ")[2]), int(app_config.conf_app_simulation_date.split(", ")[3]), int(app_config.conf_app_simulation_date.split(", ")[4]))
    else:
        currenttime = datetime.datetime.now()

    # A very hacky way of getting the lessons of current weekday
    # We add the current index of the weekday to a string with the prefix lessons_
    # The lesson_x variables were assigned before
    today = str(currenttime.weekday() + 1)
    tomorrow = str(currenttime.weekday() + 2)
    lessons_ = "lessons_"
    today_lessons = lessons_ + today
    tomorrow_lesssons = lessons_ + tomorrow
    if today_lessons in "lessons_6" or today_lessons in "lessons_7":
        return(["weekend", lessons_1])

     # Creating two variables called today_lessons and tomorrow_lessons which are a list of the lessons on that day
    today_lessons = locals()[today_lessons]
    tomorrow_lesssons = locals()[tomorrow_lesssons]

    # Check if school is over already
    if currenttime > datetime.datetime(now.year, now.month, now.day, 15, 30):
        return(["over", tomorrow_lesssons])

    # Check if school has started
    if currenttime < datetime.datetime(now.year, now.month, now.day, 8, 00):
        return(["school_starting", [today_lessons[0], times[0]]])

    # 1. First, we loop through the list of times.
    # 2. Then, we check if the current time is greater than the time in the list and less than the lesson end time.
    # 3. If it is , we calculate the time until the lesson ends and return the lesson name and time until the lesson ends.
    # 4. If it isn’t, we check if the current time is less than the next lesson time.
    # First, we iterate through the list of times.
    for time in times:
        # Then, we calculate the lesson end time by adding 45 minutes to the start time.
        lesson_end = time + timedelta(minutes=45)
        # Next, we check if the current time is between the start time and the lesson end time.
        if currenttime.time() > time.time() and currenttime.time() < lesson_end.time():
            # If it is, it calculates the time until the lesson ends.
            time_until_lesson_end = lesson_end - currenttime
            lessons_remaining = today_lessons
            # Then, we calculate the number of lessons remaining by subtracting the current time from the last lesson end time.
            lessons_remaining = lessons_remaining[times.index(time)+1:]
            new_lessons_remaining = []
            # Finally, we create a new list of the remaining lessons by iterating through the list of remaining lessons and adding the start time and lesson to a new list.
            for index, lesson in enumerate(lessons_remaining):
                try:
                    new_lessons_remaining.append(
                        [times[times.index(time) + index + 1], lesson])
                except:
                    pass

            info = [["lesson_ending", today_lessons[times.index(
                time)], time_until_lesson_end.total_seconds()], new_lessons_remaining]
            # ...and return the lesson name and time until the lesson ends
            return(info)

        # Check if the current time is before lesson start time
        if currenttime.time() < time.time():
            # If it is, get the next lesson and time until it
            next_lesson = times[times.index(time)]
            time_until_next_lesson = next_lesson - currenttime

            # Get remaining lessons today
            lessons_remaining = today_lessons
            lessons_remaining = lessons_remaining[times.index(time)+1:]
            new_lessons_remaining = []
            for index, lesson in enumerate(lessons_remaining):
                try:
                    new_lessons_remaining.append(
                        [times[times.index(time) + index + 1], lesson])
                except:
                    pass

            info = [["lesson_starting", next_lesson,
                     time_until_next_lesson.total_seconds()], new_lessons_remaining]
            return(info)
