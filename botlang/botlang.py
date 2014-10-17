# encoding: utf-8

from __future__ import unicode_literals
import string
import random
from pattern.en import tag, singularize, pluralize, comparative, superlative, lemma, lexeme, conjugate
from pattern.en.wordlist import PROFANITY

import json
import os

ENGLISH_WORDS = list(open("resources/wordlist.txt", "r").read().split())
MAX_SYLLABLES = 5

class Bot:
    def __init__(self):
        pass

    def gen_english(self):
        english = random.choice(ENGLISH_WORDS)
        return english

    def gen_bottish(self):

        # temporary silly orthography
        vowel = ("i", "í", "e", "a", "u")
        cons = ("s", "r", "t", "f", "ċ", "d", "l", "n", "p")

        bottish = ""
        new_cons = ""
        new_vowel = ""
        prev_syllables = []
        for i in range(random.randint(1, MAX_SYLLABLES)):
            new_cons = random.choice(cons)
            new_vowel = random.choice(vowel)

            if len(bottish) > 0 and bottish[len(bottish) - 1] in vowel:
                while new_vowel in prev_syllables:
                    new_vowel = random.choice(vowel)
                while new_cons in prev_syllables:
                    new_cons = random.choice(cons)

                bottish += (new_cons + new_vowel)
                prev_syllables.extend([new_cons, new_vowel])

            elif len(bottish) > 0 and bottish[len(bottish) - 1] in cons:
                while new_vowel in prev_syllables:
                    new_vowel = random.choice(vowel)
                while new_cons in prev_syllables:
                    new_cons = random.choice(cons)

                bottish += (new_vowel + new_cons)
                prev_syllables.extend([new_vowel, new_cons])

            # randomly select whether word starts with cons or vowel
            # yes, it is confusing having these statements last since they 
            # get executed first
            elif random.randint(1, 2) == 1:
                bottish += (new_cons + new_vowel)
                prev_syllables.extend([new_cons, new_vowel])

            else:
                bottish += (new_vowel + new_cons)
                prev_syllables.extend([new_vowel, new_cons])

        return bottish

    def check(self, word, dictionary):
        # check word isn't already in use (generalised for both langs)
        for definition in dictionary:
            if definition["bottish"] == word or definition["english"] == word or word in PROFANITY:
                return False

        return True

    def posify(self, bottish, english, dictionary):
        # TODO incomplete - add more tags!
        tags = {
            ("NN", "NNS"): "noun",
            ("NNP", "NNPS"): "prop. noun",
            "CC": "conj.",
            "DT": "det.",
            "JJ": "adj.",
            ("PRP", "PRP$"): "pers. pron",
            ("RB", "RBS"): "adv.",
            "UH": "interj.",
            ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ"): "verb"
        }

        pos = ""
        for key in tags.keys():
            if tag(english)[0][1] in key:
                pos = tags[key]

        if pos == "noun":
            bottish = self.pluralify(bottish, english, dictionary)
        elif pos == "adj.":
            bottish = self.adjectify(bottish, english, dictionary)
        #elif pos == "verb":
        #    bottish = self.conjugify(bottish, english, dictionary)

        return [bottish, pos]

    def adjectify(self, bottish, english, dictionary):

        comp = "foo"
        sup = "far"

        for definition in dictionary:
            # if english word is the comparative form of an existing word
            if english == comparative(definition["english"]):
                bottish = definition["bottish"] + comp
                return bottish
            # or is the superlative form of an existing word
            elif english == superlative(definition["english"]):
                bottish = definition["bottish"] + sup
                return bottish
            # or is the normal form of an existing comparative form
            elif comparative(english) == definition["english"]:
                bottish = definition["bottish"].rstrip(comp)
                return bottish
            # or is the normal form of an existing superlative form
            elif superlative(english) == definition["english"]:
                bottish = definition["bottish"].rstrip(sup)
                return bottish

        return bottish

    def pluralify(self, bottish, english, dictionary):
        plural_suffix = "ly"

        for definition in dictionary:
            # if English word is a plural
            if tag(english)[0][1] in ("NNS", "NNPS"):
                # if the singular English word is already defined...
                if singularize(english) == definition["english"]:
                    bottish = definition["bottish"] + plural_suffix
                    return bottish
                # otherwise generate a new plural
                else:
                    bottish = bottish + plural_suffix
                    return bottish

            # if English word is a singular...
            elif tag(english)[0][1] in ("NN", "NNP"):
                # if a plural version is already defined...
                if pluralize(english) == definition["english"]:
                    bottish = definition["bottish"].rstrip(plural_suffix)
                    return bottish

        return bottish

    # not going to happen :(
    #def conjugify(self, bottish, english, dictionary):
    #    # past/present/future suffixes

    #    pst = "bar"
    #    prs = "baz"
    #    fut = "bam"

    #    # if english verb is not the lemma form...
    #    if lemma(english) != english:
    #        for definition in dictionary:
    #            # check if the lemma is already in the dictionary
    #            if lemma(english) == definition["english"]:
    #                #TODO find out what form of the verb it is and append appropriate suffix to bottish word
    #                bottish = definition["bottish"] + suffix
    #                return bottish

    #    return bottish


    def add_to_dict(self, bottish, english, existing_words):
        # store multiple dictionaries (each corresponding to a word definition) in a list
        all_words = []

        new_word = {"bottish":bottish, "english":english}

        # check if file empty and read in existing definitons accordingly
        if os.stat("dictionary.json").st_size > 0 :
            all_words.append(new_word)
            for d in existing_words:
                all_words.append(d)
        else: 
            all_words.append(new_word)

        # write out each definition to the file again
        with open("dictionary.json", "w") as fp:
            json.dump(all_words, fp)


    def run(self):

        dictionary = {}

        # create file if it doesn't exist
        if not (os.path.exists("dictionary.json")):
            with open("dictionary.json", "w") as fp:
                json.dump(dictionary, fp)

        with open("dictionary.json") as fp:
            dictionary = json.load(fp)

        # I think having 2 loops may actually be more efficient cause of the break
        english = self.gen_english()
        for i in range(0, 100):
            if not self.check(english, dictionary):
                english = self.gen_english()
                if i == 99:
                    print "ran out of english words!"
            else:
                break

        bottish = self.gen_bottish()
        # we don't want bottish imitating english (pity this couldn't be done in check())
        for i in range(0, 100):
            if bottish in ENGLISH_WORDS:
                bottish = self.gen_bottish()
                if i == 99:
                    print "ran out of valid bottish words!"

            if not self.check(bottish, dictionary):
                bottish = self.gen_bottish()
                if i == 99:
                    print "ran out of valid bottish words!"

            else:
                break

        bottish, pos = self.posify(bottish, english, dictionary)[0], self.posify(bottish, english, dictionary)[1]
        self.add_to_dict(bottish, english, dictionary)

        return ("{bot} ({p}): {eng}").format(
            bot=bottish,
            eng=english,
            p=pos
        )


if __name__ == "__main__":
    bot = Bot()
    print bot.run()

