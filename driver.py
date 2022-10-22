from buffer import load_buffer
from lex import tokenize

if __name__ == "__main__":
    token = []
    lexeme = []

    # tokenize
    for i in load_buffer():
        t, lex = tokenize(i)
        token += t
        lexeme += lex

    res = ", ".join(set(token))
    print("\n\n Unique tokens: \n", res)
