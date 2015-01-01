from syntax import PARENTHESES, OPERATORS, DELIMS
import random

def generate_condition():
    def generate_comparison():
        return "{x1} {comp} {x2}".format(
            x1 = str(random.randint(1, 100)), 
            comp = random.choice(OPERATORS["comparison"]),
            x2 = str(random.randint(1, 100))
        )

    def generate_logic():
        return " {comp} {logic} ".format(
            comp = generate_comparison(),
            logic = random.choice(OPERATORS["logical"])
        )

    return random.choice([
        generate_comparison(), 
        generate_logic() * random.randint(1, 3) + generate_comparison()]
    )

def generate_body(TABS):
    TABS += 1
    if random.random() < 0.5:
        return "\t" * TABS + if_statement(TABS)
    else:
        return "{tabs}return x{__delim}".format(
            tabs = "\t" * TABS,
            __delim = random.choice(["", random.choice(DELIMS)])
        )

def if_statement(TABS=0):
    pattern = "if {__open_p}{condition}{__close_p} {__open_block}\n{body}\n{tabs}{__close_block}"

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
        __open_p = __OPEN_P,
        condition = CONDITION,
        __close_p = __CLOSE_P,
        __open_block = __OPEN_BLOCK,
        body = BODY,
        tabs = "\t" * TABS,
        __close_block = __CLOSE_BLOCK
    )

    return construct

def gen():
    functions = [
        if_statement()
    ]

    return random.choice(functions)

if __name__ == "__main__":
    print gen()
