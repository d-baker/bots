# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import random
import string

class Winter:
    def __init__(self):
        pass

    def rainstorm(self):
        chars = [
            "💧",
            "☁",
            ]

        #spaces = [
        #    "\u2003",
        #    "\u2002",
        #    " " * random.randint(2, 5)
        #    ]

        rainstorm = ""

        chance = random.random()

        if chance > 0.8:
            rainstorm += (" " * random.randint(3, 10)) + "⚡" # lightning

        # 140 minus possible extra 2 chars (unicode) added later
        while sum(1 if c in string.whitespace else 2 for c in rainstorm) < 138:

            rainstorm += "{cloud_spaces}{cloud_chars}{cloud_spaces}{cloud_newlines}{cloud_newlines}{droplet_spaces}{droplets}{droplet_spaces}{droplet_newlines}".format(
               cloud_spaces=" " * random.randint(1, 10),
               cloud_chars=random.choice(chars),
               cloud_newlines="\n" * random.randint(0, 1),
               droplet_spaces=" " * random.randint(0, 10),
               droplets="💧" * random.randint(0, 1),
               droplet_newlines="\n" * random.randint(0, 1)
            )

        if random.random() > 0.6:
            rainstorm += "☔"

        return rainstorm


    def snowstorm(self):
        chars = [
            "⁕", 
            "❄ ", 
            "❅ ", 
            " ❆  ", 
            ]

        snowstorm = ""

        # standard whitespace = 1 char, unicode = 2 chars, 
        # 140 minus up to 26 extra chars added later
        while sum(1 if c in string.whitespace else 2 for c in snowstorm) < 114:

            snowstorm += "{bigflake_spaces}{bigflakes}{bigflake_spaces}{bigflake_newlines}{newlines}{tinyflake_spaces}{dots}{tinyflake_spaces}{tinyflake_newlines}".format(
                bigflake_spaces=" " * random.randint(1, 10),
                bigflakes=random.choice(chars),
                bigflake_newlines="\n" * random.randint(0, 1),
                newlines="\n" * random.randint(0, 1),
                tinyflake_spaces=" " * random.randint(0, 10),
                dots="·" * random.randint(0, 1),
                tinyflake_newlines="\n" * random.randint(0, 1)
            )

        # conditions:
        # if snowman, maybe tree
        # if tree rather than snowman, maybe little house and maybe snowman 
        # (all 3 possible together) 
        # note: confused about weighting, so probably not quite the way I want it

        if random.random() < 0.2:
            snowstorm += "☃" # snowman
            if random.random() < 0.4:
                snowstorm += (" " * random.randint(5, 10)) + "🌲" # tree


        elif random.random() < 0.3:
            snowstorm += (" " * random.randint(5, 10)) + "🌲" # tree
            if random.random() < 0.3:
                snowstorm += (" " * random.randint(5, 10)) + "🏠" # little house
            if random.random() < 0.2:
                snowstorm += (" " * random.randint(5, 10)) + "☃" # snowman

        return snowstorm

if __name__ == "__main__":
    bot = Winter()
    print bot.snowstorm()
