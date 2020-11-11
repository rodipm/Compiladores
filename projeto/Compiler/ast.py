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
    __doc__ = "Representacao de uma lista de comandos em um bloco"
    def __init__(self):
        self.children = []


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

class IfStatement(AST):
    __doc__ = 'Representação de um IF statement'
    def __init__(self, left_exp, operator, right_exp, line):
        self.left_exp = left_exp
        self.operator = operator
        self.right_exp = right_exp
        self.line = line

class NoOp(AST):
    pass