#* encoding: utf-8 *#

#! /usr/bin/env python3

import random

LINE_LENGTH = 20
SEA_LINES = 4
SKY_LINES = 2

# sun and moon currently look best when they're at the top of the skyline,
# but this could change if for example we change the number of lines
SUN_HEIGHT = 0
MOON_HEIGHT = 0

SUN_REPETITIONS = 1 # until we land on some weird planet with multiple suns
MOON_REPETITIONS = 1 # until we land on some weird planet with multiple moons
STAR_REPETITIONS = 4

BIG_WAVE_REPETITIONS = 5
FLOATABLES_REPETITIONS = 1 # only want 1 of each floatable on a line for now

WAVE_CHAR = "~";
BIG_WAVE_CHAR = "〜"

FLOATABLES = {
    "🛥" : 10, # boat
    "🌊" : 20, # massive wave
    "🐬" : 40, # dolphin
    "🐟" : 30, # fish
    "🐠" : 20, # tropical fish
}

SUNS = [
    "⛅",
    "☀",
    "☼",
    "🌅", # sunrise
    "🌤", # white sun with small cloud
    "🌦", # white sun behind cloud with rain
    "🌥" # white sun behind cloud
]

MOONS = [
    "🌙",
    "🌑",
    "🌕",
    "☽",
    "☾",
    "🌒",
    "🌓",
    "🌔",
    "🌖",
    "🌗",
    "🌘"
]

STARS = {
    "✦" : 30,
    "✧" : 20,
    "*" : 40,
    "." : 60,
    #"★" : 15,
    #"☆" : 7,
    #"✭" : 7,
    #"✮" : 4,
    #"✴" : 15,
    #"✶" : 20,
}

################################################################################

# add a special character at a random position, a given number of times
# mostly used with a repetition of 1 for single objects like sun or moon
def add_char(line, char, repetitions):
    repetitions = round(repetitions)

    for rep in range(repetitions):
        extra_position = random.choice(range(LINE_LENGTH))
        line = line[ : extra_position ] + char + line[ (extra_position+1) : ]

    return line

# add big waves to a line
def add_big_waves(line, repetitions):
    repetitions = round(repetitions)

    for rep in range(repetitions):
        extra_position = random.choice(range(LINE_LENGTH))
        line = line[ : extra_position ] + BIG_WAVE_CHAR + line[ (extra_position+1) : ]

    return line

# add multiple weighted random characters to a line, i.e. stars, floatables
def add_weighted_chars(line, char_dict, repetitions):
    random_num = random.randint(0, 100)

    for rep in range(repetitions):
        char = random.choice( list(char_dict.keys()) )
        weight = char_dict[char]

        if random_num < weight:
            extra_position = random.choice(range(LINE_LENGTH))
            line = line[ : extra_position ] + char + line[ (extra_position+1) : ]

    return line

# add special characters (big waves, floatables) to water
def float_boat(line):
    line = add_big_waves(line, BIG_WAVE_REPETITIONS)
    line = add_weighted_chars(line, FLOATABLES, FLOATABLES_REPETITIONS)
    return line

################################################################################

def generate_day_sky():
    sky = [" " * LINE_LENGTH] * SKY_LINES

    sun = random.choice(SUNS)
    sky[SUN_HEIGHT]  = add_char(sky[SUN_HEIGHT], sun, SUN_REPETITIONS)

    return "\n".join(sky)

def generate_night_sky():
    sky = [" " * LINE_LENGTH] * SKY_LINES
    sky = [add_weighted_chars(line, STARS, STAR_REPETITIONS) for line in sky]

    moon = random.choice(MOONS)
    sky[MOON_HEIGHT] = add_char(sky[MOON_HEIGHT], moon, MOON_REPETITIONS)

    return "\n".join(sky)


def generate_sky(time_of_day):
    sky = generate_day_sky() # day is default

    if time_of_day == "night":
        sky = generate_night_sky()

    return sky

def generate_sea():
    water = [(WAVE_CHAR * LINE_LENGTH)] * SEA_LINES
    water = [float_boat(line) for line in water]
    return "\n".join(water)

################################################################################

def generate_seascape():
    time_of_day = random.choice(["night", "day"])

    sky = generate_sky(time_of_day)
    sea = generate_sea()

    seascape = sky + "\n" + sea

    return seascape


print (generate_seascape())
