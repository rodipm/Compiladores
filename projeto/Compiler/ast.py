class AST(object):
    pass

class BinOp(AST):
    __doc__ = "Representacao de operacoes binarias do tipo opreando OPERADOR operando"
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    __doc__ = "Representacao de numeros na AST"
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST):
    __doc__ = "Representacao de operacoes unarias +/-"
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class StatementList(AST):
    __doc__ = "Representacao da lista de comandos dentro do programa"
    def __init__(self):
        self.children = [] #BaseStatements

class BaseStatement(AST):
    __doc__ = "Representacao de linhas numeradas do programa"
    def __init__(self, line_number, node):
        self.line_number = line_number
        self.node = node

class Assign(AST):
    __doc__ = "Representacao de uma operacao de definicao de variavel"
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    __doc__ = 'Representacao de uma variavel'

    def __init__(self, token):
        self.token = token
        self.value = token.value

class PrintStatement(AST):
    __doc__ = 'Representação de um comando de PRINT'
    def __init__(self):
        self.children = []

class PrintItem(AST):
    __doc__ = 'Representação de um item de PRINT'
    def __init__(self, token):
        self.token = token

class GotoStatement(AST):
    __doc__ = 'Representação de um comando de desvio GOTO'
    def __init__(self, destination_line):
        self.destination_line = destination_line

class IfStatement(AST):
    __doc__ = 'Representação de um IF statement'
    def __init__(self, left_exp, operator, right_exp, destination_line):
        self.left_exp = left_exp
        self.operator = operator
        self.right_exp = right_exp
        self.destination_line = destination_line

class NoOp(AST):
    pass