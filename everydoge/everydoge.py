import string
import random
import sys
from pattern.en import tag
from pprint import pprint

# TODO 
# avoid multiple occurrences of the same prefix
# randomise whether interjection is added or not

def dogeify():
    verbs = list(open("resources/verbs.txt").read().split())
    adjectives = list(open("resources/adjectives.txt").read().split())
    singular = list(open("resources/singular.txt").read().split())
    plurals = list(open("resources/plural.txt").read().split())

    vprefix = ["very", "much", "many", "such", "so"]
    aprefix = ["such", "much"]
    sprefix = ["so", "very", "many", "such"]
    pprefix = ["much"]

    interjections = ("wow", "amaze", "excite")

    if random.randint(1, 6) == 1:
        bottish = ("{very} {verb}. {much} {adjective}. {so} {singular}, {interjection}.").format(
            very=random.choice(vprefix), 
            verb=random.choice(verbs), 

            so=random.choice(sprefix), 
            singular=random.choice(singular), 

            much=random.choice(pprefix),
            adjective=random.choice(adjectives),

            interjection=random.choice(interjections)
        )
    else:
        bottish = ("{very} {verb}. {much} {adjective}. {so} {singular}.").format(
            very=random.choice(vprefix), 
            verb=random.choice(verbs), 

            so=random.choice(sprefix), 
            singular=random.choice(singular), 

            much=random.choice(pprefix),
            adjective=random.choice(adjectives),
        )

    print bottish

if __name__=="__main__":
    for i in range(0, 10):
        dogeify()

