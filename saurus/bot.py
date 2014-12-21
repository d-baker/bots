import random
from tweeter import tweet

suffixes = ["saurus", "don", "ilia", "sauriform", "raptor", "ceratops", "saura", "ryx"]
prefixes = []

with open ("resources/dinosaurs.txt") as fp:
    for word in fp.read().split():
        w = word
        for suffix in suffixes:
            if suffix in word:
                w = word.replace(suffix, "")

        prefixes.append(w)


def gen():
    p = random.choice(prefixes)
    s = random.choice(suffixes)
    if p[len(p) - 1] == s[0]:
        s = s[1:]

    return p + s

if __name__ == "__main__":
    #for i in range (0, 10):
    #    print gen()
    tweet(gen())
