import random

class Bugfix:
    name = "bugfix.log"

    def __init__(self):
        pass;

    def gen(self):
        formats = list(open("resources/formats.txt").readlines())
    
        singular = list(open("resources/singular.txt").read().split()) 
        plural = list(open("resources/plural.txt").read().split()) 
        verb = list(open("resources/verb.txt").read().split())
        verbing = list(open("resources/verbing.txt").read().split())
    
        return random.choice(formats).strip().format(
            nouns1 = random.choice(plural),
            verb = random.choice(verb),
            verbing = random.choice(verbing),
            nouns2 = random.choice(plural)
        )

if __name__ == "__main__":
    bugfix_log = Bugfix()
    for i in range(0, 10):
        print bugfix_log.gen()
