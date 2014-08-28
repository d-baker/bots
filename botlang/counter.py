# encoding: utf-8

from __future__ import unicode_literals

import json
import os

def main():
    dictionary = {}
    words = []

    with open("resources/dictionary.json") as fp:
        dictionary = json.load(fp)

    for definition in dictionary:
        if len(definition["bottish"]) <= 3:
            definition["len"] = "2-3"
        elif len(definition["bottish"]) <= 5:
            definition["len"] = "4-5"
        elif len(definition["bottish"]) < 7:
            definition["len"] = "6-7"

        if "len" in definition:
            words.append(definition)

    with open("resources/countdata.txt", "w") as fp:            
        print("============================================================")
        print("VERY SHORT")
        print("============================================================\n")
        for definition in words:
            if definition["len"] == "2-3":
                print ("Bottish: {} | English: {}".format(
                    definition["bottish"],
                    definition["english"])
                )

        print("\n============================================================")
        print("MODERATELY SHORT")
        print("============================================================\n")
        for definition in words:
            if definition["len"] == "4-5":
                print ("Bottish: {} | English: {}".format(
                    definition["bottish"],
                    definition["english"])
                )

        print("\n============================================================")
        print("SOMEWHAT SHORT")
        print("============================================================\n")
        for definition in words:
            if definition["len"] == "6-7":
                print ("Bottish: {} | English: {}".format(
                    definition["bottish"],
                    definition["english"])
                )



if __name__ == "__main__":
    main()
