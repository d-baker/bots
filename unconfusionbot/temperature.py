# encoding: utf-8
from __future__ import unicode_literals
from resources.config import  WEATHER_KEY
import requests
import json

# weather data provided by http://openweathermap.org
def request(location):
    url = "http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={key}".format(city=location, key=WEATHER_KEY)
    r = requests.get(url)

    js = json.loads(r.text)
    return js["main"]["temp"]

def test():
    request("Melbourne")

if __name__ == "__main__":
    test()
