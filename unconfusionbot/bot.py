# encoding: utf-8
from __future__ import unicode_literals

import json
import tweepy
import re

from datetime import datetime, timedelta
from pytz import timezone
from temperature import request
import pytz

from resources.config import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET
import twitter

class UnconfusionBot:

    def __init__(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
        auth.set_access_token(TOKEN,SECRET)
        self.api = tweepy.API(auth)

    def get_mentions(self):
        # TODO only retrieves one mention
        # need to check for age of tweet
        for mention in tweepy.Cursor(self.api.mentions_timeline).items(1):
            return mention

    def get_username(self, mention):
        return mention.user.screen_name

    def get_location(self, username):
        user_info = self.api.get_user(screen_name = username)
        location = user_info.location

        loc_strings = list( re.split(",/", location) )

        if len(loc_strings) > 1:
            timezone = loc_strings[1].strip() + "/" + loc_strings[0].strip()
        else:
            timezone = loc_strings[0]

        return timezone

    def get_timezone(self, mention):
        tweet = mention.text

        # TODO need to get rid of @-string
        tweet_strings = list(re.split('\s|,|/', tweet))
        print tweet_strings

        timezones = list(open("resources/timezones.txt", "r").read().split())
        tz = []
        timezone = ""

        for s in tweet_strings:
            tz = [t for t in timezones if s.lower() in t.lower()]

        if len(tz) == 0:
            self.log("couldn't find a valid timezone in tweet");
            return
        else:
            # first timezone matching something in the tweet
            timezone = tz[0]

        return timezone

    def get_relative_time(self, foreign, local):
        # TODO use regex to identify a time to convert in tweet

        # regex "\d:\d" (not taking into account possible AM/PM)
        local_tz = timezone(local)
        local_time = datetime.now(local_tz) # change this bit

        if foreign == None:
            return "couldn't find that timezone, sorry"

        foreign_tz = timezone(foreign)
        foreign_time = local_time.astimezone(foreign_tz)

        return foreign_time.strftime('%b %d, %I:%M %p')

    def get_current_time(self, foreign):
        if foreign == None:
            return "couldn't find that timezone, sorry"

        foreign_tz = timezone(foreign)
        foreign_time = datetime.now(foreign_tz)

        return foreign_time.strftime('%b %d, %I:%M %p')

    ##########################################################################

    def unconfuse_timezone(self, mention, username):
        local_tz = self.get_location(username)
        foreign_tz = self.get_timezone(mention)
        text = ""

        if "current" in mention.text:
            text = self.get_current_time(foreign_tz)
        else:
            text = self.get_relative_time(foreign_tz, local_tz)

        self.tweet(text, mention)

    def unconfuse_temperature(self, mention, username):
        location = self.get_location(username)
        temp = request(location)
        text = "{t}°C".format(t = temp)
        self.tweet(text, mention)

    def log(self, message):
        time = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        print ("{t} | {m}".format(t = time, m = message))

    def tweet(self, text, mention):
        status = "@{u} {t}".format(u = mention.user.screen_name, t = text)
        in_reply_to = mention.id

        #s = self.api.update_status(status, in_reply_to)

        self.log("tweeted \"{t}\"".format(t = status))

    def run(self):
        mention = self.get_mentions()
        mention_text = mention.text.replace("@tempntime_bot", "")
        username = self.get_username(mention)

        if "time" in mention_text:
            self.unconfuse_timezone(mention, username)
        elif "temp" in mention_text:
            self.unconfuse_temperature(mention, username)


if __name__ == "__main__":
    bot = UnconfusionBot()
    bot.run()
