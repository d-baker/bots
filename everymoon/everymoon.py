# encoding: utf-8
from __future__ import unicode_literals
from moondate import MoonDate
import json
import os

from resources.config import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, SECRET
import twitter


def tweet(emoji):
    auth = twitter.OAuth(TOKEN, SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    t = twitter.Twitter(auth=auth)

    t.statuses.update(status=emoji)


def run():
    moon = MoonDate("southern")

    ############################ STATE READING #############################

    state = [{"phase": moon.get_phase(), "tweeted": False}]

    # open file if it exists and isn't empty, otherwise create and write to it
    if os.path.exists("resources/state.json") and os.stat("resources/state.json").st_size > 0:
        with open ("resources/state.json", "r") as fp:
            data = json.load(fp)
            for d in data:
                state.append(d)
    else:
        with open ("resources/state.json", "w") as fp:
            json.dump(state, fp)

    for d in state:
        if d["phase"] == moon.get_phase() and d["tweeted"] == True:
            print "already tweeted, skipping"
            return


    ############################### TWEETING ##############################

    emoji = moon.get_emoji()
    tweet(emoji)
    moon.log("info", "tweeted {phase} emoji".format(phase=moon.get_phase()))
    state[0]["tweeted"] = True


    ############################ STATE SAVING #############################

    with open ("resources/state.json", "w") as fp:
        if moon.get_phase() == "new moon": # delete file and start over
            os.remove("resources/state.json")

        json.dump(state, fp)


if __name__ == "__main__":
    run()
