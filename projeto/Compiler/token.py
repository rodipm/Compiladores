INTEGER, PLUS, MINUS, MUL, DIV, EQUAL, LPAREN, RPAREN, LET = (
    'INTEGER',
    'PLUS',
    'MINUS',
    'MUL',
    'DIV',
    '=',
    '(',
    ')',
    'LET'
)

RESERVED_KEYWORDS = {
    'LET':Token('LET', 'LET'),
}

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

