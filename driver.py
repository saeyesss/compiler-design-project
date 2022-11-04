from buffer import load_buffer
from lex import tokenize
from parser import parse_grammar, items, print_info, process_input
if __name__ == "__main__":
    # # LEXICAL ANALYSIS PHASE
    # token = []
    # lexeme = []
    #
    # # tokenize
    # for i in load_buffer():
    #     t, lex = tokenize(i)
    #     token += t
    #     lexeme += lex
    #
    # res = ", ".join(set(token))
    # print("\n\n Unique tokens: \n", res)

    # PARSING PHASE
    parse_grammar()
    items()
    global parse_table
    print_info()
    process_input()
