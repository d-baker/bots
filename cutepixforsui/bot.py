 #!/usr/bin/env python3

import tweepy
import time
from datetime import datetime
from resources.config import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(TOKEN, SECRET)
api = tweepy.API(auth)

# seconds between each RT
INTERVAL = 30

def get_hashtag_tweets():
    already_tweeted = open("resources/tweeted.dat").readlines()
    sui_id = api.get_user(screen_name="swayandsea").id_str
    trusted_users = api.followers_ids(screen_name="swayandsea") + [sui_id]

    hashtags=["#catpicturesforsui", "#catpixforsui", "#catpix4sui", "#cuteanimalsforsui"]

    all_tweets = []

    for tag in hashtags:
        tweets = api.search(q=tag)

        for i in range(0, len(tweets)):
            if tweets[i] != None:
                if tweets[i].author.id_str in trusted_users and tweets[i].id_str not in already_tweeted:
                    all_tweets += [tweets[i].id]

    return all_tweets

def run():
    tweets = get_hashtag_tweets()
    log("retrieved latest tweets")

    while (tweets != []):
        just_tweeted = api.retweet(tweets.pop())
        log("retweeted a tweet")

        with open("resources/tweeted.dat", "a") as fp:
            log("last retweet ID written to file")
            fp.write(just_tweeted + "\n")

        log("sleeping for " + INTERVAL + " seconds")
        time.sleep(INTERVAL)

def log(message):
    date = datetime.utcnow().strftime("%Y-%m-%e %T") 
    return "{} | {}".format(date, message)

if __name__ == "__main__":
    log("bot initialised")
    while True:
        run()
