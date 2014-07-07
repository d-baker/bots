from resources.config import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET
import twitter

def tweet(word):
    auth = twitter.OAuth(TOKEN, SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    t = twitter.Twitter(auth=auth)

    t.statuses.update(status=word)
    #print word

