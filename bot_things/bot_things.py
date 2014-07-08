
import random
import os

words = open("resources/everyword.txt").read().split()
count = 0

def gen():

    if (os.path.exists("resources/tweeted_words.txt")):
        tweeted_words = list(open("resources/tweeted_words.txt").read().strip()) # read file
    else:
        tweeted_words = open("resources/tweeted_words.txt", "w+") # create file

    # keep generating words until one that hasn't been picked before turns up
    word = random.choice(words).strip()
    while word in tweeted_words:
        word = random.choice(words).strip()

    if (os.path.exists("resources/tweeted_words.txt")):
        tweeted_words = open("resources/tweeted_words.txt", "a") # append to file
    else:
        tweeted_words = open("resources/tweeted_words.txt", "w") # create file

    # add latest word to file
    tweeted_words.write(word + "\n")

    # bot variation
    special_prefixes = ("computer ", "robot ", "processor ", "syntax ", "compiler ", "algorithm ")

    phrase = ""

    if random.random() < 0.02:

        if random.random() < 0.1:
            phrase = random.choice(special_prefixes) + " " + word
        else:
            phrase = word + " " + random.choice(special_prefixes)

    elif random.random() < 0.1:
        phrase = word + " bot"

    else:
        phrase = "bot " + word


    return phrase


if __name__ == "__main__":
    print gen()
