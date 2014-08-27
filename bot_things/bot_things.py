# encoding: utf-8
from __future__ import unicode_literals
import random
import os
from datetime import date

# this should really be in a class but oh well

NOUNS = open("resources/nouns.txt").read().split()
ADJECTIVES = open("resources/adjectives.txt").read().split()
EVERYWORD = open("resources/everyword.txt").read().split()

def gen():

    if (os.path.exists("resources/tweeted_words.txt")):
        tweeted_words = list(open("resources/tweeted_words.txt").read().split()) # read file
    else:
        tweeted_words = open("resources/tweeted_words.txt", "w+") # create file

    # bot variation
    special_prefixes = ("computer", "robot", "processor", "syntax", "compiler", "algorithm")

    word = ""
    phrase = ""

    # high chance of "{subject} {noun}"
    if random.random() > 0.02:
        word = random.choice(NOUNS).strip()

        for i in range (0, 100):
            if word in tweeted_words:
                word = random.choice(NOUNS).strip()

                # give up and use everyword list if we sort-of run out of words
                if i == 99:
                    word = last_resort(word, tweeted_words)


        # high chance of using "bot"
        if random.random() > 0.02:
            phrase = "bot " + word
        # small chance of using something else
        else:
            phrase = random.choice(special_prefixes) + " " + word


    # small chance of "{adjective} {subject}"
    else:
        word = random.choice(ADJECTIVES).strip()

        for i in range (0, 100):
            if word in tweeted_words:
                word = random.choice(NOUNS).strip()

                # give up and use everyword list if we sort-of run out of words
                if i == 99:
                    word = last_resort(word, tweeted_words)

        # high chance of using "bot"
        if random.random() > 0.02:
            phrase = word + " bot"
        # small chance of using something else
        else:
            phrase = word + " " + random.choice(special_prefixes)

    # append to file if it exists
    if (os.path.exists("resources/tweeted_words.txt")):
        words = open("resources/tweeted_words.txt", "a")
    # create file otherwise
    else:
        words = open("resources/tweeted_words.txt", "w")

    # add latest word to file
    words.write(word + "\n")

    return phrase


def last_resort(word, tweeted_words):
    word = random.choice(EVERYWORD).strip()
    for i in range(0, 100):
        if word in tweeted_words:
            word = random.choice(EVERYWORD).strip()

            # even everyword gives up sometimes
            if i == 99:
                log("bot apocalypse")
                return

        return word


def log(message):
    today = "{day}/{month}/{year}".format(
        day=date.today().day, 
        month=date.today().month, 
        year=date.today().year)

    print "{d}: {m}".format(d=today, m=message)


if __name__ == "__main__":
    print gen()
