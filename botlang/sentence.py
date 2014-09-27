# encoding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
import string
import random
from pattern.en import tag, singularize, pluralize, comparative, superlative, lemma, lexeme, conjugate
from pattern.en.wordlist import PROFANITY

import json
import os

class Sentence:
    def __init__(self):
        self.dictionary = {}
        with open("resources/dictionary.json") as fp:
            self.dictionary = json.load(fp)

    def translate(self, sentence):
        print ("English: " + sentence)
        sentence = list(sentence.split())
        text = ""

        print ("Bottish: ", end="")
        for word in sentence:
            translation = "N/A"
            for definition in self.dictionary:
                if definition["english"] == word:
                    translation = definition["bottish"]
            text += translation + " "

        return(text)

    def get_sentence(self):
        sentences = open("resources/botlang-sentences.txt").readlines()
        s = random.choice(sentences)
        print (self.translate(s))

if __name__ == "__main__":
    sentence = Sentence()
    sentence.get_sentence()
