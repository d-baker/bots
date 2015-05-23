# encoding: utf-8
from __future__ import unicode_literals

from tweeter import tweet

def bot():
    current_word = ""
    with open ("resources/everyword.txt") as fp:
        current_word = fp.readline().strip().decode("utf-8")
    tweet(umlautify(current_word[::-1]))
    # if tweeting fails the current word shouldn't get deleted
    with open("resources/everyword.txt", "r") as fin:
        words = fin.read().splitlines(True)
    with open("resources/everyword.txt", "w") as fout:
        fout.writelines(words[1:])

def umlautify(word):
    return ''.join(c if c == ' ' else c + u'\u0308' for c in word)

if __name__ == "__main__":
    bot()
