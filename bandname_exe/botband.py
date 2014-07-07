import random

def gen():
    of_prefix = list(open("resources/of_prefixes.txt", "r").read().split())
    of_postfix = list(open("resources/of_postfixes.txt", "r").read().split())
    the_prefix = list(open("resources/the_prefixes.txt", "r").read().split())
    the_postfix = list(open("resources/the_postfixes.txt", "r").read().split())

    options = (random.choice(of_prefix) + " of " + random.choice(of_postfix), random.choice(the_prefix) + " the " + random.choice(the_postfix))
    text = random.choice(options)

    return text

