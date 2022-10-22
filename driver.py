from buffer import load_buffer
from lex import LexicalAnalyser

if __name__ == "__main__":
    Analyser = LexicalAnalyser()

    token = []
    lexeme = []
    row = []
    col = []

    # tokenize
    for i in load_buffer():
        t, lex, line, column = Analyser.tokenize(i)
        token += t
        lexeme += lex
        row += line
        col += column

    print("\n\n Unique tokens: \n\n", set(token))
