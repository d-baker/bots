# encoding: utf-8
from __future__ import unicode_literals

import json
import tweepy
import re
import time

from datetime import datetime, timedelta
from pytz import timezone
import requests
import pytz

from resources.config import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET
import twitter

# THANKYOU www.geonames.org for the data!

class UnconfusionBot:

    def __init__(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
        auth.set_access_token(TOKEN,SECRET)
        self.api = tweepy.API(auth)

    # TODO only retrieves one mention!
    # also need to check for age of tweet
    def get_mentions(self):
        for mention in tweepy.Cursor(self.api.mentions_timeline).items(1):
            return mention

    def get_username(self, mention):
        return mention.user.screen_name

    # TODO needs to be much more flexible - can't really assume last word
    # in tweet will always be the location
    def get_location(self, mention):
        tweet_strings = list(re.split('\s|,|/', mention.text))
        return tweet_strings[len(tweet_strings)-1]

    def get_lat_long(self, location):
        url = "http://api.geonames.org/searchJSON?name={}&username=dbaker".format(location)
        r = requests.get(url)
        lat = ""
        lng = ""

        js = json.loads(r.text)
        for result in js["geonames"]:
            if result["toponymName"] == location:
                lat = result["lat"]
                lng = result["lng"]
                return [lat, lng];

        return False

    def get_timezone(self, location):
        coords = self.get_lat_long(location)

        if coords:
            url = "http://api.geonames.org/timezoneJSON?lat={}&lng={}&username=dbaker".format(coords[0], coords[1])

            r = requests.get(url)

            js = json.loads(r.text)
            time = js["time"]
            s = datetime.strptime(time, "%Y-%m-%d %H:%M")
            return s.strftime("%Y-%m-%d, %I:%M %p")

        return False

    def get_temp(self, location):
        coords = self.get_lat_long(location)

        if coords:
            url = "http://api.geonames.org/findNearByWeatherJSON?lat={}&lng={}&username=dbaker".format(coords[0], coords[1])

            r = requests.get(url)

            js = json.loads(r.text)
            temp = js["weatherObservation"]["temperature"]
            return temp

        return False

    ##########################################################################

    def log(self, message):
        time = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        print ("{t} | {m}".format(t = time, m = message))

    def tweet(self, text, mention):
        status = "@{u} {t}".format(u = mention.user.screen_name, t = text)
        in_reply_to = mention.id

        s = self.api.update_status(status, in_reply_to)

        self.log("tweeted \"{t}\"".format(t = status))

    def run(self):
        while True:
            try:
                mention = self.get_mentions()
                mention_text = mention.text.replace("@tempntime_bot", "")
                username = self.get_username(mention)
                location = self.get_location(mention)

                if "time" in mention_text:
                    self.tweet(self.get_timezone(location), mention)
                elif "temp" in mention_text:
                    self.tweet(self.get_temp(location) + "°C", mention)

                time.sleep(10)

            except tweepy.TweepError:
                time.sleep(15 * 60)


if __name__ == "__main__":
    bot = UnconfusionBot()
    bot.run()
