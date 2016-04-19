#! /usr/bin/env python3

from resources.config import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET
import twitter

def tweet(s):
    auth = twitter.OAuth(TOKEN, SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    t = twitter.Twitter(auth=auth)

    charfix = "." # fix twitter whitespace bug
    if s[:1] == " ":
        s = charfix + s[1:] 

    if len(s) < 140:
        print("Tweeting...")
        print(s)
        t.statuses.update(status=s)
    else:
        print("Tweet to long")
