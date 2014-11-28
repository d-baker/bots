import tweepy
from resources.testconfig import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET
from datetime import datetime, date
import random

def authorize():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(TOKEN, SECRET)
    return tweepy.API(auth)

def current_date():
    day = datetime.today().day
    month = datetime.today().month
    year = datetime.today().year

    return "{}-{}-{}".format(year, month, day) 

def log(message):
    with open ("log.txt", "a") as fp:
        fp.write(current_date() + " | " + message + "\n")

def tweet():
    colors = []
    tweeted_colors = []

    with open ("grayscale.txt") as fp:
        colors = list(line.strip() for line in fp.readlines())

    with open ("tweeted_colors.txt", "w+") as fp:
        tweeted_colors = list(line.strip() for line in fp.readlines())

    color = random.choice(colors)
    # this is awful
    for i in range(0, 100):
        if color in tweeted_colors:
            if i == 99:
                log("ran out of colors")
            else:
                color = random.choice(colors)
        else:
            break

    api = authorize()
    api.update_with_media(color[1:] + ".png", status=color)

    with open ("tweeted_colors.txt", "a") as fp:
        fp.write(color + "\n")

if __name__ == "__main__":
    tweet()
    #log("hi")
