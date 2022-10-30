from buffer import load_buffer
from lex import tokenize
from parser import *
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

    # PARSING PHASE
    parse_grammar()
    items()
    global parse_table
    parse_table = [[""] for c in range(len(terminals) + len(nonterminals) + 1)for r in range(len(C))]
    print_info()
    process_info()
