import re


class LexicalAnalyser:
    # row number
    line_no = 1

    def tokenize(self, code):
        rules = [
            ('MAIN', r'main'),  # main
            ('INT', r'int'),  # int
            ('FLOAT', r'float'),  # float
            ('IF', r'if'),  # if
            ('ELSE', r'else'),  # else
            ('PRINT', r'printf'),  # print
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
            ('FORMAT', r'\%[cdsfe]'), # format specifier
            ('FLOAT_CONST', r'\d(\d)*\.\d(\d)*'),  # floating point numbers
            ('INTEGER_CONST', r'\d(\d)*'),  # integers
            ('COMMENT', r'/\*.*?\*/'), # comment
            ('NEWLINE', r'\n'),  # NEW LINE
            ('SKIP', r'[ \t]+'),  # tabs and spaces
            ('MISMATCH', r'.'),  # any other char

        ]

        token = []
        lexeme = []
        row = []
        column = []

        tokens_join = "|".join('(?P<%s>%s)' % x for x in rules)
        line_start = 0

        for n in re.finditer(tokens_join, code):
            token_type = n.lastgroup
            token_lexeme = n.group(token_type)

            if token_type == 'NEWLINE':
                line_start = n.end()
                self.line_no += 1
            elif token_type == 'SKIP':
                continue
            elif token_type == 'MISAMATCH':
                raise RuntimeError('%r unexpected on line %d' % (token_lexeme, self.line_no))
            else:
                col = n.start() - line_start
                column.append(col)
                token.append(token_type)
                lexeme.append(token_lexeme)
                row.append(self.line_no)

                print('token = {0},\t\tlexeme = \'{1}\''.format(token_type,token_lexeme))

        return token, lexeme, row, column
