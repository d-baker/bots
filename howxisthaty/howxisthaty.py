import random
import os
from tweeter import tweet

def gen():
    adjectives = list(open("resources/adjectives.txt"))
    nouns = list(open("resources/nouns.txt"))

    phrase = ("how {adjective} is that {noun}").format(
        adjective = random.choice(adjectives).strip(),
        noun = random.choice(nouns).strip()
        )

    if random.random() <= 0.2:
        phrase += "!"

    if os.path.exists("resources/tweeted.txt"):
        tweeted = list(open("resources/tweeted.txt", "r").read().split())
        if phrase in tweeted:
            print ("error: already tweeted that one")

    tweet(phrase)
    with open("resources/tweeted.txt", "a") as fp:
        fp.write(phrase + "\n")


if __name__ == "__main__":
    gen()
