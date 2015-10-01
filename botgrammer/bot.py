from syntax import PARENTHESES, OPERATORS, DELIMS, VARNAMES, TYPES
import random

def generate_condition():
    def generate_comparison():
        return "{x1} {comp} {x2}".format(
            x1 = random.choice( [ random.choice(VARNAMES), str(random.randint(1, 100)) ] ), 
            comp = random.choice(OPERATORS["comparison"]),
            x2 = random.choice( [ random.choice(VARNAMES), str(random.randint(1, 100)) ] ), 
        )

    def generate_logic():
        return "{comp} {logic} ".format(
            comp = generate_comparison(),
            logic = random.choice(OPERATORS["logical"])
        )

    return random.choice([
        generate_comparison(), 
        generate_logic() * random.randint(1, 2) + generate_comparison()]
    )

""" TODO 
- do/while loop
- while loop
- for loop
- variable assignment statements

def conditional_statement(keyword="if", TABS=0):

    def generate_body(TABS):
        TABS += 1
        if random.random() < 0.5:
            return "\t" * TABS + conditional_statement("if", TABS)
        else:
            return "{tabs}return {var}{__delim}".format(
                tabs = "\t" * TABS,
                var = random.choice( [ random.choice(VARNAMES), str(random.randint(1, 100)) ] ),
                __delim = random.choice(["", random.choice(DELIMS)])
            )

    pattern = "{k} {__open_p}{condition}{__close_p} {__open_block}\n{body}\n{tabs}{__close_block}"

    __OPEN_P = random.choice(PARENTHESES["open"])
    while __OPEN_P == ":":
        __OPEN_P = random.choice(PARENTHESES["open"])
    index = PARENTHESES["open"].index(__OPEN_P)
    __CLOSE_P = PARENTHESES["close"][index]

    CONDITION = generate_condition()
    BODY = generate_body(TABS)

    __OPEN_BLOCK = random.choice(PARENTHESES["open"])
    index = PARENTHESES["open"].index(__OPEN_P)
    __CLOSE_BLOCK = PARENTHESES["close"][index]
    if __OPEN_BLOCK == ":":
        __CLOSE_BLOCK = ""

    construct = pattern.format(
        k = keyword,
        __open_p = __OPEN_P,
        condition = CONDITION,
        __close_p = __CLOSE_P,
        __open_block = __OPEN_BLOCK,
        body = BODY,
        tabs = "\t" * TABS,
        __close_block = __CLOSE_BLOCK
    )

    if random.random() < 0.3:
        # TODO why is the indentation for this bit too deep?
        # also plain "else" can't be followed by a condition
        construct += " " + conditional_statement(random.choice(["elif", "else if"]), TABS+1)

    return construct

def chars_ok(code):
    if len(code) >= 140:
        return False
    return True

def gen():
    functions = [
        conditional_statement()
    ]

    return random.choice(functions)

if __name__ == "__main__":
    code = gen()
    while not (chars_ok(code)):
        print "too many chars"
        code = gen()
    else:
        print code
