INTEGER, PLUS, MINUS, MUL, DIV, EQUAL, LPAREN, RPAREN, LET, ID, REM, EOF, PRINT, COMMA, IF, THEN, EQ = (
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
    'IF',
    'THEN',
    '=='
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
    'IF':Token('IF', 'IF'),
    'THEN':Token('THEN', 'THEN')
}