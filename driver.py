from buffer import load_buffer
from lex import tokenize
from parser import parse_main

if __name__ == "__main__":
    # LEXICAL ANALYSIS PHASE
    token = []
    lexeme = []

    # tokenize
    for i in load_buffer():
        t, lex = tokenize(i)
        token += t
        lexeme += lex

    res = ", ".join(set(token))
    print("\n\n Unique tokens: \n", res)
    print("\n\n")

    # PARSING PHASE
    parse_main()
