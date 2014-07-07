import random
import os
from tweeter import tweet

def gen():
    adjectives = list(open("resources/adjectives.txt"))
    nouns = list(open("resources/nouns.txt"))

    phrase = ""
    if random.random() > 0.2:
        phrase = ("how {adjective} is that {noun}!").format(
            adjective = random.choice(adjectives).strip(),
            noun = random.choice(nouns).strip()
            )
    else:
        phrase = ("how {adjective} is that {noun}").format(
            adjective = random.choice(adjectives).strip(),
            noun = random.choice(nouns).strip()
            )

    if os.path.exists("resources/tweeted.txt"):
        with open("resources/tweeted.txt", "r") as tweeted:
            if phrase in tweeted:
                print ("error: already tweeted that one")

    tweet(phrase)
    with open("resources/tweeted.txt", "a") as tweeted:
        tweeted.write(phrase + "\n")


if __name__ == "__main__":
    gen()
