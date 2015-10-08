 #!/usr/bin/env python3

import os
import random
import tweepy
import time
from datetime import datetime
from resources.config import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(TOKEN, SECRET)
api = tweepy.API(auth)

# seconds between each RT
RT_INTERVAL = 180 # 3 mins
# seconds between each search update
UPDATE_INTERVAL = 3600 # 1 hr

def get_hashtag_tweets():
    already_tweeted = open("resources/tweeted.dat").readlines()

    trusted_users = [name.strip() for name in open("resources/trusted_users.dat").readlines()]

    hashtags=["#catpicturesforsui", "#catpixforsui", "#catpix4sui", "#cuteanimalsforsui"]

    all_tweets = []

    for tag in hashtags:
        tweets = api.search(q=tag, rpp=10)

        for i in range(0, len(tweets)):
            if tweets[i] != None:
                if tweets[i].entities["urls"] != [] and tweets[i].author.screen_name in trusted_users and tweets[i].id_str not in already_tweeted:
                    all_tweets += [int(tweets[i].id_str)]

    return all_tweets

def run():
    log("attempting scheduled image post")
    post_scheduled_image()

    tweets = []

    try:
        tweets = get_hashtag_tweets()
        log("retrieved latest tweets")
    except:
        log("an error occurred while attempting to retrieve tweets")
        return

    while (tweets != []):
        try:
            api.retweet(id=tweets[0])
            log("retweeted a tweet with ID " + str(tweets[0]))

            with open("resources/tweeted.dat", "a") as fp:
                fp.write(str(tweets[0]) + "\n")
                tweets.pop(0)
                log("last retweet ID written to file")

            log("sleeping for " + str(RT_INTERVAL) + " seconds between RTs")
            time.sleep(RT_INTERVAL)

        except tweepy.error.TweepError as e:
            log("an error occurred while trying to RT, skipping")
            tweets.pop(0)

def log(message):
    date = datetime.utcnow().strftime("%Y-%m-%e %T") 
    print ("{} | {}".format(date, message))

def test(tweetID):
    api.retweet(id=tweetID)
    log("RT'd")

def post_scheduled_image():
    scheduled_status = [
     "meow",
     ":3",
     "what a weird umbrella",
     "relationship goals",
     "this could be us but ur a table",
     "never date a stem boy",
     "boys r bad",
     "destroy all whites",
     "strange house here",
     "what a quaint piglet!",
     "wow, what a beautiful lamp!",
     "what an unusual library",
     "never date an atheist",
     "insert white person joke here",
     "lol cishets",
     "lol men",
     "white ppl r such a lol",
     "insert misandry here",
     "#ThisIsWhatAnEngineerLooksLike",
     "#FeministsAreUgly? more like... cats",
     "😻", "😺", "😸", "😼", "😽", "🙀", "😹", "🐯", "🐱", "🐈", "🐅", "🐆"]
    image_files = os.listdir("resources/scheduled_images")

    if len(image_files) > 0:
        photo = "resources/scheduled_images/" + image_files[0]
        api.update_with_media(filename=photo, status=random.choice(scheduled_status))
        os.remove(photo)

    log("scheduled image posted")

if __name__ == "__main__":
    log("bot initialised")

    while True:
        run()

        log("sleeping for " + str(UPDATE_INTERVAL) + " seconds between search updates")
        time.sleep(UPDATE_INTERVAL)
