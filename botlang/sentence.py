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
        pass

    def load_dict(self):
        with open("dictionary.json") as fp:
            return json.load(fp)

    def translate(self, sentence):
        entities = ["&amp;", "&lt;", "&gt;"]

        bot = Bot()

        print ("English: " + sentence)
        sentence = list(sentence.split())
        text = ""

        for word in sentence:
            translation = "N/A"

            # just the word, no punctuation
            stripped_word = re.sub(r"[^a-zA-Z]", "", word)

            # find the word and translate it
            for definition in self.load_dict():
                if definition["english"] == stripped_word:
                    translation = definition["bottish"]

            # no existing translation? bot learns a new word!
            if translation == "N/A":
                translation = (bot.run(bot.gen_bottish(), word))[0]

            # if the "word" was only punctuation it'll be empty
            # so only concatenate translation if there's a word
            if stripped_word:

                # keep smileys, entities
                if re.search(r"((:|;).{1,3})|(\w{1,2}(:|;))", word) or (word in entities):
                    print ("probably a smiley, keep it");
                    translation = word

                elif re.search(r"'[a-zA-Z]$", word):
                    print("probably an abbreviation, delete punctuation")
                    translation = word.replace(word, translation)

                # replace non-punctuation part of string with translation
                elif re.search(r"(^[^a-zA-Z])|([^a-zA-Z]$)", word):
                    print("word contains punctuation, keep it")
                    translation = word.replace(stripped_word, translation)

                # concatenate with full sentence
                text += translation + " "

            else:
                print("all punctuation, don't substitute anything")
                text += word + " "

        print("Bottish: " + text)
        return(text)

    #pick a random sentence from a file
    def get_sentence(self):
        sentences = open("resources/botlang-sentences.txt").readlines()
        s = random.choice(sentences)
        return (self.translate(s))

if __name__ == "__main__":
    sentence = Sentence()
    #sentence.translate("foobar")
