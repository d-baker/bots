from resources.config import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET
import twitter
import random
from winter import Winter

# this file is just to make testing the bot easier and is not actually used for deployment
def tweet():
    auth = twitter.OAuth(TOKEN, SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    t = twitter.Twitter(auth=auth)

    tweet = ""
    bot = Winter()
    #if random.random() > 0.3:
    #    tweet = bot.snowstorm()
    #else:
    #    tweet = bot.rainstorm()

    tweet = bot.rainstorm()
    #tweet = bot.snowstorm()

    t.statuses.update(status=tweet)
    #print tweet

if __name__ == "__main__":
    tweet()

