import random

ANIMALS = list(open("animals.txt").read().split())

PARENTHESES = {
    "open": [
        "{",
        "(",
        "[",
        ":"
    ], 
    "close": [
        "}",
        ")",
        "]",
        ""
    ]
}

OPERATORS = {
    "arithmetic": [
        "+",
        "-",
        "/",
        "*",
        "**",
        "%"
    ],
    "assignment": [
        "=",
        "+=",
        "-=",
        "/=",
        "*=",
        "**=",
        "%="
    ],
    "comparison": [
        "==",
        "===",
        ">",
        "<",
        ">=",
        "<=",
        "!==",
        "!===",
        "!>",
        "!<",
        "!>=",
        "!<="
    ],
    "logical": [
        "&&",
        "||",
        "and",
        "or",
    ]
}

DELIMS = [
    ";",
]

VARNAMES = [
    "foo",
    "bar", 
    "baz",
    "bam",
    "x", 
    "y",
    "z",
    "n",
    "num", 
    "counter",
    random.choice(ANIMALS),
    random.choice(ANIMALS),
    random.choice(ANIMALS),
    random.choice(ANIMALS),
    random.choice(ANIMALS)
]

TYPES = [
    "string",
    "int",
    "float",
    "double",
    "array"
]
