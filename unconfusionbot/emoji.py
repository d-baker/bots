#encoding: utf-8*
from __future__ import unicode_literals
from __future__ import print_function
import random
from datetime import datetime

class Emojifier:
    NUM_LINES = 5

    zero="###\n#.#\n#.#\n#.#\n###\n"
    one="#\n#\n#\n#\n#\n"
    two="###\n..#\n###\n#..\n###\n"
    three="###\n..#\n###\n..#\n###\n"
    four="#.#\n#.#\n###\n..#\n..#\n"
    five="###\n#..\n###\n..#\n###\n"
    six="###\n#..\n###\n#.#\n###\n"
    seven="###\n..#\n..#\n..#\n..#\n"
    eight="###\n#.#\n###\n#.#\n###\n"
    nine="###\n#.#\n###\n..#\n..#\n"

    numerals = {
        "0": list(zero.split()),
        "1": list(one.split()), 
        "2": list(two.split()), 
        "3": list(three.split()), 
        "4": list(four.split()), 
        "5": list(five.split()), 
        "6": list(six.split()), 
        "7": list(seven.split()), 
        "8": list(eight.split()), 
        "9": list(nine.split())
        }
    
    def __init__(self):
        pass

    def emojify_temp(self, temp):
        degree=list("##\n##\n..\n..\n..\n".split())
        c=list("###\n#..\n#..\n#..\n###\n".split())

        cold_emojis = [
            "☁",
            "💧",
            "☔",
            "☂",
            "⛈",
            "⛸"
        ]
        hot_emojis = [
            "☀",
            "🔥",
            "🍦"
        ]

        final_string = ""
    
        num_one = ""
        num_two = ""
    
        if len(temp) == 1:
            num_one = Emojifier.numerals[temp[0]]
        elif len(temp) == 2:
            num_one = Emojifier.numerals[temp[0]]
            num_two = Emojifier.numerals[temp[1]]
    
        for i in range(0, Emojifier.NUM_LINES):
            if len(temp) == 1:
                final_string += (num_one[i] + "." + degree[i] + "." + c[i] + "\n")
            elif len(temp) == 2:
                final_string += (num_one[i] + "." + num_two[i] + "." + degree[i] + "." + c[i] + "\n")
    
        if int(temp) < 17:
            return self.convert(final_string, random.choice(cold_emojis))
        elif int(temp) > 23:
            return self.convert(final_string, random.choice(hot_emojis))
        return self.convert(final_string)
    
    def emojify_time(self, cur_time):
        cur_time = cur_time.strftime("%H:%M")
    
        colon=list("...\n.#.\n...\n.#.\n...\n".split())

        time_string = cur_time.replace(":", "")
        if time_string[0] == "0":
            time_string = time_string[1:]
    
        num_one = ""
        num_two = ""
        num_three = ""
        num_four = ""
    
        if len(time_string) == 3:
            num_one = Emojifiernumerals[time_string[0]]
            num_two = Emojifier.numerals[time_string[1]]
            num_three = Emojifier.numerals[time_string[2]]
        elif len(time_string) == 4:
            num_one = Emojifier.numerals[time_string[0]]
            num_two = Emojifier.numerals[time_string[1]]
            num_three = Emojifier.numerals[time_string[2]]
            num_four = Emojifier.numerals[time_string[3]]
    
        final_string = ""
    
        for i in range(0, Emojifier.NUM_LINES):
            if len(time_string) == 3:
                final_string += (num_one[i] + colon[i] + num_two[i] + "." + num_three[i] + "\n")
            elif len(time_string) == 4:
                final_string += (num_one[i] + "." + num_two[i] + colon[i] + num_three[i] + "." + num_four[i] + "\n")
    
        return self.convert(final_string)
    
    def convert(self, string, em = None):
        # not all emojis work - some aren't the same width as the whitespace emoji.
        # always test first!
    
        # TODO make separate emoji list for temp
        emojis=["💧",
                "☁",
                "⚡",
                "☔",
                "🌲",
                "🐌",
                "👾",
                "💀",
                "👽",
                "🏡",
                ]
    
        whitespace="\u2B1C"
 
        if em:
            emoji = em
        else:
            emoji = random.choice(emojis)
    
        string = string.replace(".", whitespace)
        string = string.replace("#", emoji)
        return string

