# encoding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
import string
import random
from pattern.en import tag, singularize, pluralize, comparative, superlative, lemma, lexeme, conjugate
from pattern.en.wordlist import PROFANITY

import json
import os
import re

from botlang import Bot

class Sentence:
    def __init__(self):
        self.dictionary = {}
        with open("dictionary.json") as fp:
            self.dictionary = json.load(fp)

    def translate(self, sentence):
        bot = Bot()

        print ("English: " + sentence)
        sentence = list(sentence.split())
        text = ""

        print ("Bottish: ", end="")
        for word in sentence:
            translation = "N/A"
            stripped_word = re.sub(r"\W+", "", word)

            for definition in self.dictionary:
                if definition["english"] == stripped_word:
                    translation = definition["bottish"]

            if translation == "N/A":
                translation = (bot.run(bot.gen_bottish(), word))[0]

            translation = word.replace(stripped_word, translation)

            text += translation + " "

        return(text)

    def get_sentence(self):
        sentences = open("resources/botlang-sentences.txt").readlines()
        s = random.choice(sentences)
        return (self.translate(s))

if __name__ == "__main__":
    sentence = Sentence()
    sentence.get_sentence()
