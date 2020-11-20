INTEGER, PLUS, MINUS, MUL, DIV, EQUAL, LPAREN, RPAREN, LET, ID, REM, EOF, PRINT, COMMA, GOTO, GO, TO, IF, THEN, EQ, NOTEQ, GT, LESS, GTEQ, LESSEQ, FOR, TO, STEP, NEXT, DEF, FN, READ, QUOTE, STRING, OPENBRACKET, CLOSEBRACKET, DIM, STRING, RND, GOSUB, RETURN= (
    'INTEGER',
    'PLUS',
    'MINUS',
    'MUL',
    'DIV',
    '=',
    '(',
    ')',
    'LET',
    'ID',
    'REM',
    'EOF',
    'PRINT',
    'COMMA',
    'GOTO',
    'GO',
    'TO',
    'IF',
    'THEN',
    '==',
    "<>",
    ">",
    "<",
    ">=",
    "<=",
    "FOR",
    "TO",
    "STEP",
    "NEXT",
    "DEF",
    "FN",
    "READ",
    "\"",
    "STRING",
    "OPENBRACKET",
    "CLOSEBRACKET",
    "DIM",
    "STRING",
    "RND",
    "GOSUB",
    "RETURN"
)

class Token(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """
        Representação do Token em String
        """
        return 'Token({type}, {value})'.format(type=(self.type),
          value=(repr(self.value)))

    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS = {
    'LET':Token('LET', 'LET'),
    'REM':Token('REM', 'REM'),
    'PRINT':Token('PRINT', 'PRINT'),
    'GOTO': Token('GOTO', 'GOTO'),
    'GO': Token('GO', 'GO'),
    'TO': Token('TO', 'TO'),
    'IF':Token('IF', 'IF'),
    'THEN':Token('THEN', 'THEN'),
    'FOR':Token('FOR', 'FOR'),
    'TO':Token('TO', 'TO'),
    'STEP':Token('STEP', 'STEP'),
    'NEXT':Token('NEXT', 'NEXT'),
    'DEF':Token('DEF', 'DEF'),
    'FN': Token('FN', 'FN'),
    'READ': Token('READ', 'READ'),
    'DIM': Token('DIM', 'DIM'),
    'RND': Token('RND', 'RND'),
    'GOSUB': Token('GOSUB', 'GOSUB'),
    'RETURN': Token('RETURN', 'RETURN'),
}