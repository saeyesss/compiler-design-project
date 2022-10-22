import re


def tokenize(code):
    rules = [
        ('MAIN', r'main'),  # main
        ('INT', r'int'),  # int
        ('FLOAT', r'float'),  # float
        ('IF', r'if'),  # if
        ('ELSE', r'else'),  # else
        ('PRINT', r'printf'),  # printf
        ('LBRACKET', r'\('),  # (
        ('RBRACKET', r'\)'),  # )
        ('LBRACE', r'\{'),  # {
        ('RBRACE', r'\}'),  # }
        ('COMMA', r','),  # ,
        ('PCOMMA', r';'),  # ;
        ('EQ', r'=='),  # ==
        ('NE', r'!='),  # !=
        ('LE', r'<='),  # <=
        ('GE', r'>='),  # >=
        ('LT', r'<'),  # <
        ('GT', r'>'),  # >
        ('ID', r'[a-zA-Z]\w*'),  # identifiers
        ('FORMAT', r'\%[cdsfe]'),  # format specifier
        ('FLOAT_CONST', r'\d(\d)*\.\d(\d)*'),  # floating point numbers
        ('INTEGER_CONST', r'\d(\d)*'),  # integers
        ('COMMENT', r'\/\/.*'),  # single line comment
        ('NEWLINE', r'\n'),  # newline
        ('SKIP', r'[ \t]+'),  # tabs and spaces
        ('QUOTE', r'\"|\''),  # single / double quote
        ('MISMATCH', r'.'),  # any other char
    ]

    token = []
    lexeme = []

    tokens_join = "|".join('(?P<%s>%s)' % x for x in rules)

    for n in re.finditer(tokens_join, code):
        token_type = n.lastgroup
        token_lexeme = n.group(token_type)

        if token_type == 'NEWLINE' or token_type == 'SKIP':
            continue
        elif token_type == 'MISMATCH':
            raise RuntimeError('unexpected token %r in the src file' % token_lexeme)
        else:
            token.append(token_type)
            lexeme.append(token_lexeme)

            print('token = {0},\t\tlexeme = \'{1}\''.format(token_type, token_lexeme))

    return token, lexeme
