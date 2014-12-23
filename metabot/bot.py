import twitter
import time
import random
#from resources.testconfig import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET
from resources.config import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET

# store each line of source in a list
def get_lines():
    lines = []
    with open ("bot.py") as fp:
        lines = [line.strip() for line in fp.readlines() if line.strip() != ""]

    return lines

def tweet(word):
    auth = twitter.OAuth(TOKEN, SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    t = twitter.Twitter(auth=auth)

    t.statuses.update(status=word)

def log(message):
    date = time.strftime("%Y/%m/%d")

    with open ("bot.log", "a+") as fp:
        fp.write( "{} | {}\n".format(date, message) )

def run_me():
    tweeted_lines = []
    with open ("tweeted_lines.txt", "a+") as fp:
        tweeted_lines = [line.strip() for line in fp.readlines()]

    lines = get_lines()

    # falls back to the first line of source if all lines have been tweeted
    counter = 0
    chosen_line = lines[counter]

    while chosen_line in tweeted_lines:
        counter += 1

        # avoid infinite loop if all lines have been tweeted
        if counter >= len(lines):
            return

        chosen_line = lines[counter]

    log("tweeting \"{}\"".format(chosen_line))
    tweet(chosen_line)

    # as each line is tweeted, it gets appended to the tweeted_lines file
    with open ("tweeted_lines.txt", "a") as fp:
        fp.write(chosen_line + "\n")

def test():
    length = len(get_lines())
    for i in range (0, length):
        run_me()

if __name__ == "__main__":
    #test()
    run_me()
