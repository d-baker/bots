# encoding: utf-8
from __future__ import unicode_literals

# emoji reference: http://apps.timwhitlock.info/emoji/tables/unicode#block-1-emoticons

CATEGORIES = {
    "human_faces": {"start_range", "1f601", "end_range": "1F637"},
    "cat_faces": {"start_range", "1f638", "end_range": "1F640"}
}

def get_array(cat):
    start_range = CATEGORIES[cat]["start_range"]
    end_range = CATEGORIES[cat]["end_range"]

    array = []
    for i in range(int(start_range, 16), int(end_range, 16)):
        hexcode = str(hex(i))
        unicode_string = "\\u" + hexcode[2:]
        array.append(unicode_string)

    return array

if __name__ == "__main__":
    print get_array()
