# encoding: utf-8

from __future__ import unicode_literals
import string
import random
from pattern.en import tag, singularize, pluralize, comparative, superlative, lemma, lexeme, conjugate
from pattern.en.wordlist import PROFANITY

import json
import os


def main():
    dictionary = {}

    with open("resources/dictionary.json") as fp:
        dictionary = json.load(fp)

    for definition in dictionary:
        if len(definition["bottish"]) < 7:
            print definition

    with open("resources/count.txt", "w") as fp:
        json.dump(definition, fp)

if __name__ == "__main__":
    main()
