import configparser
import os

config_obj = configparser.ConfigParser()
__location__ = os.path.realpath(
os.path.join(os.getcwd(), os.path.dirname(__file__)))
config_obj.read(os.path.join(__location__, 'appconfig.ini'))
conf_app = config_obj["app"]
conf_app_debug = conf_app["debug"]
conf_app_date_simulation = conf_app["date_simulation"]
conf_app_simulation_date = conf_app["simulation_date"]
classes_url = conf_app["classes_url"]
timetable_url = conf_app["timetable_url"]