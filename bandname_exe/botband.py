import random

def gen():
    nouns = list(open("resources/nouns.txt", "r").read().split())
    adjectives = list(open("resources/adjectives.txt", "r").read().split())

    of_prefix = list(open("resources/of_prefixes.txt", "r").read().split())
    of_postfix = list(open("resources/of_postfixes.txt", "r").read().split())
    the_prefix = list(open("resources/the_prefixes.txt", "r").read().split())
    the_postfix = list(open("resources/the_postfixes.txt", "r").read().split())


    normal_options = (

        "{noun} of {nouns}".format(
            noun = random.choice(of_prefix),
            nouns = random.choice(of_postfix)
        ),

        "{verb} the {noun}".format(
            verb = random.choice(the_prefix),
            noun = random.choice(the_postfix)
        )

    )


    silly_options = (

        "{noun} of {adjective} {nouns}".format(
            noun = random.choice(of_postfix),
            adjective = random.choice(adjectives),
            nouns = random.choice(nouns)
        ),

        "{verb} the {adjective} {noun}".format(
            verb = random.choice(the_prefix),
            adjective = random.choice(adjectives),
            noun = random.choice(nouns)
        )

    )


    text = ""

    if random.random() < 0.08:
        text = random.choice(silly_options)
    else:
        text = random.choice(normal_options)

    return text

if __name__ == "__main__":
    for i in range (0, 10):
        print gen()

