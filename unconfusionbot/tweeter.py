#!/usr/bin/env python2
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import json
import re
import time

from datetime import datetime, timedelta
from pytz import timezone
import requests
import pytz
import random

from resources.config import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET
#from resources.testconfig import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET

from twitterbot import TwitterBot
from emoji import Emojifier

class UnconfusionBot(TwitterBot):
    def bot_init(self):
        """
        Initialize and configure your bot!

        Use this function to set options and initialize your own custom bot
        state (if any).
        """

        ############################
        # REQUIRED: LOGIN DETAILS! #
        ############################
        self.config['api_key'] = CONSUMER_KEY
        self.config['api_secret'] = CONSUMER_SECRET
        self.config['access_key'] = TOKEN
        self.config['access_secret'] = SECRET


        ######################################
        # SEMI-OPTIONAL: OTHER CONFIG STUFF! #
        ######################################

        MINS = 60 
        SECS = 60
        # how often to tweet, in seconds
        # tweet every 3 hours
        self.config['tweet_interval'] = 3 * MINS * SECS

        # use this to define a (min, max) random range of how often to tweet
        # e.g., self.config['tweet_interval_range'] = (5*60, 10*60) # tweets every 5-10 minutes
        self.config['tweet_interval_range'] = None

        # only reply to tweets that specifically mention the bot
        self.config['reply_direct_mention_only'] = False

        # only include bot followers (and original tweeter) in @-replies
        self.config['reply_followers_only'] = True

        # fav any tweets that mention this bot?
        self.config['autofav_mentions'] = False

        # fav any tweets containing these keywords?
        self.config['autofav_keywords'] = []

        # follow back all followers?
        self.config['autofollow'] = False


        ###########################################
        # CUSTOM: your bot's own state variables! #
        ###########################################
        
        # If you'd like to save variables with the bot's state, use the
        # self.state dictionary. These will only be initialized if the bot is
        # not loading a previous saved state.

        # self.state['butt_counter'] = 0

        # You can also add custom functions that run at regular intervals
        # using self.register_custom_handler(function, interval).
        #
        # For instance, if your normal timeline tweet interval is every 30
        # minutes, but you'd also like to post something different every 24
        # hours, you would implement self.my_function and add the following
        # line here:
        
        # self.register_custom_handler(self.my_function, 60 * 60 * 24)


    def on_scheduled_tweet(self):
        location = self.get_random_city()
        timezone = self.get_timezone(location)
        temp = self.get_temp(location)
        emojifier = Emojifier()

        if location:

            if random.random() < 0.5:

                if random.random() < 0.2:
                    text = location + ":\n" + emojifier.emojify_temp(temp)
                else:
                    text = location + ":\n" + emojifier.emojify_time(datetime.strptime(timezone, "%Y-%m-%d, %I:%M %p"))

            else:
                text = location + ": " + timezone + " / " + temp + "°C"

            self.post_tweet(text)

    def on_mention(self, tweet, prefix):
        tweet_time = tweet.created_at # tweet timestamp
        now = datetime.utcnow()
        diff = now - tweet_time # tweet age

        text = ""

        # only reply to mentions in last 4 mins
        if diff.seconds <= 240:
            location = self.get_location(tweet.text)
            coords = self.get_lat_long(location)
            timezone = self.get_timezone(location)
            temp = self.get_temp(location)
            emojifier = Emojifier()

            mention = re.sub(r'(^|[^@\w])@(\w{1,15})\b', "", tweet.text)

            if "time" in mention:
                if "temp" in mention:
                    text = location + ": " + timezone + " / " + temp + "°C"
                elif "emoji" in mention and coords:
                    text = location + ":\n" + emojifier.emojify_time(datetime.strptime(timezone, "%Y-%m-%d, %I:%M %p"))
                else:
                    text = location +  ": " + location

            elif "temp" in mention:
                if "emoji" in mention and coords:
                    text = location + ":\n" + emojifier.emojify_temp(temp)
                else:
                    text = location + ": " + temp + "°C"

            # provide both by default if unspecified
            else:
                text = location + ": " + timezone + " / " + temp + "°C"

            if coords:
                if "emoji" in mention:
                    self.post_tweet(prefix + "\n" + text, reply_to=tweet)
                else:
                    self.post_tweet(prefix + ' ' + text, reply_to=tweet)


    def on_timeline(self, tweet, prefix):
        """
        Defines actions to take on a timeline tweet.

        tweet - a tweepy.Status object. You can access the text with
        tweet.text

        prefix - the @-mentions for this reply. No need to include this in the
        reply string; it's provided so you can use it to make sure the value
        you return is within the 140 character limit with this.

        It's up to you to ensure that the prefix and tweet are less than 140
        characters.

        When calling post_tweet, you MUST include reply_to=tweet, or
        Twitter won't count it as a reply.
        """
        # text = function_that_returns_a_string_goes_here()
        # prefixed_text = prefix + ' ' + text
        # self.post_tweet(prefix + ' ' + text, reply_to=tweet)

        # call this to fav the tweet!
        # if something:
        #     self.favorite_tweet(tweet)

        pass

    # TODO needs to be much more flexible - can't really assume last word
    # in tweet will always be the location, or that it's only a single word
    def get_location(self, mention):
        tweet_strings = list(re.split('\s|,|/', mention))
        return tweet_strings[len(tweet_strings)-1].capitalize()

    def get_lat_long(self, location):
        url = "http://api.geonames.org/searchJSON?name={}&username=dbaker".format(location)
        r = requests.get(url)
        lat = ""
        lng = ""

        js = json.loads(r.text)

        try:
            for result in js["geonames"]:
                if result["toponymName"] == location:
                    lat = result["lat"]
                    lng = result["lng"]
                    return [lat, lng];
        except:
            pass

        return False

    def get_random_city(self):
        n = random.randint(-180, 180)
        s = random.randint(-180, 180)
        w = random.randint(-180, 180)
        e = random.randint(-180, 180)

        url = "http://api.geonames.org/citiesJSON?north={}&south={}&west={}&east=-{}&username=dbaker".format(n, s, w, e)
        r = requests.get(url)

        cities = []

        js = json.loads(r.text)

        try:
            for result in js["geonames"]:
                cities.append(result["toponymName"])

            return random.choice(cities)

        except:
            return False

    def get_timezone(self, location):
        coords = self.get_lat_long(location)

        if coords:
            url = "http://api.geonames.org/timezoneJSON?lat={}&lng={}&username=dbaker".format(coords[0], coords[1])

            r = requests.get(url)

            js = json.loads(r.text)

            try:
                time = js["time"]
                s = datetime.strptime(time, "%Y-%m-%d %H:%M")
                return s.strftime("%Y-%m-%d, %I:%M %p")
            except:
                pass

        return "sorry, something went wrong"

    def get_temp(self, location):
        coords = self.get_lat_long(location)

        if coords:
            url = "http://api.geonames.org/findNearByWeatherJSON?lat={}&lng={}&username=dbaker".format(coords[0], coords[1])

            r = requests.get(url)

            js = json.loads(r.text)
            try:
                temp = js["weatherObservation"]["temperature"]
                return temp
            except:
                pass

        return "sorry, something went wrong"

if __name__ == '__main__':
    bot = UnconfusionBot()
    bot.run()

