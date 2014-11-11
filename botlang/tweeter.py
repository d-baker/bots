
#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

from twitterbot import TwitterBot
from botlang import Bot
from sentence import Sentence
import os
import random
import re
import datetime

#from resources.testconfig import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET
from resources.config import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET

class Botlang (TwitterBot):
    def bot_init(self):
        """
        Initialize and configure your bot!

        Use this function to set options and initialize your own custom bot
        state (if any).
        """

        self.generator = Bot()
        self.sentencer = Sentence()

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
        
        MINS, HOURS = 60, 60 * 60

        # how often to tweet, in seconds
        #self.config['tweet_interval'] = 60 * 60     # default: 30 minutes

        # use this to define a (min, max) random range of how often to tweet
        # e.g., self.config['tweet_interval_range'] = (5*60, 10*60) # tweets every 5-10 minutes
        self.config['tweet_interval_range'] = (30 * MINS, 3 * HOURS)

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
        # ugh ugh ugh
        text = self.generator.format_for_tweet(self.generator.run(self.generator.gen_bottish(), self.generator.gen_english()))

        self.post_tweet(text)

    def on_mention(self, tweet, prefix):
        tweet_time = tweet.created_at # tweet timestamp
        now = datetime.datetime.utcnow()
        diff = now - tweet_time # tweet age

        # only reply to mentions in last 2 mins
        if diff.seconds <= 120:
            #mention = re.sub(r'(^|[^@\w])@(\w{1,15})\b', "", tweet.text)

            text = self.sentencer.translate(tweet.text)
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


if __name__ == '__main__':
    bot = Botlang()
    bot.run()
