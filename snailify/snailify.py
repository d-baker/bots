#encoding: utf-8

from __future__ import unicode_literals
import random
from pattern.en import tag

def is_noun(word):
    return tag(word)[0][1] == "NN"

def snailify(text):
    # deal with HTML entities
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&amp;", "&")

    snails = ["🐌", "snail"]
    questioning_snails = ["🐌?", "snail?"]

    nouns = [w.strip() for w in text.split() if is_noun(w)]

    snailified_text = text

    if nouns == [] or random.random() < 0.2:
        snailified_text = text + ". " + random.choice(questioning_snails)
    else:
        snailified_text = text.replace(random.choice(nouns), random.choice(snails))

    return snailified_text

def just_snails():
    return random.choice(["🐌" * random.randint(1, 5), "snail?"])

if __name__ == "__main__":
    for i in range(0, 10):
        print snailify("the quick brown fox jumped over the lazy dog")
        print just_snails()
