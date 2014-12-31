#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals
from twitterbot import TwitterBot
import random
from snailify import snailify, just_snails
from resources.config import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET
import re
import logging
import datetime

class MyTwitterBot(TwitterBot):
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

        # how often to tweet, in seconds
        HOUR = 60 * 60

        # 30 second interval for testing
        self.config['tweet_interval'] = 30

        # use this to define a (min, max) random range of how often to tweet
        # e.g., self.config['tweet_interval_range'] = (5*60, 10*60) # tweets every 5-10 minutes

        # tweet every 1-6 hours. such random!
        self.config['tweet_interval_range'] = (HOUR * 1, HOUR * 6)

        # only reply to tweets that specifically mention the bot
        self.config['reply_direct_mention_only'] = False

        # only include bot followers (and original tweeter) in @-replies
        self.config['reply_followers_only'] = True

        # fav any tweets that mention this bot?
        self.config['autofav_mentions'] = False

        # fav any tweets containing these keywords?
        self.config['autofav_keywords'] = ["snail", "🐌"]

        # follow back all followers?
        self.config['autofollow'] = True

        self.config['logging_level'] = logging.INFO

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

    def retweet_snails(self):
        timeline = self.get_user_timeline("poem_exe", False, 50)

        for tweet in timeline:
            if "snail" in tweet.text:
                self.retweet_tweet(tweet)
                return

    def on_scheduled_tweet(self):
        # either retweet snail haiku or tweet a random number of snail emoji
        if random.random() > 0.5:
            self.post_tweet(just_snails())
        else:
            self.retweet_snails()

    def on_mention(self, tweet, prefix):
        tweet_time = tweet.created_at # tweet timestamp
        now = datetime.datetime.utcnow()
        diff = now - tweet_time # tweet age

        # only reply to mentions in last 2 mins
        if diff.seconds <= 120:
            tweet_text = re.sub(r'^@(\w{1,15})\b', "", tweet.text)
            text = snailify(tweet_text[1:])
            self.post_tweet(prefix + ' ' + text, reply_to=tweet)

    def on_timeline(self, tweet, prefix):
        if random.random() < 0.2:
            tweet_text = re.sub(r'^@(\w{1,15})\b', "", tweet.text)
            text = snailify(tweet_text[1:])
            self.post_tweet(prefix + ' ' + text, reply_to=tweet)


        # call this to fav the tweet!
        # if something:
        #     self.favorite_tweet(tweet)

if __name__ == '__main__':
    bot = MyTwitterBot()
    bot.run()
