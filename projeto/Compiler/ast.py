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

class DimStatement(AST):
    __doc__ = "Representacao de declaração de arrays"
    def __init__(self, arr_var, arr_size):
        self.arr_var = arr_var
        self.arr_size = arr_size

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

    def __init__(self, token, scopes_list, index_exp=None):
        self.token = token
        self.value = token.value
        self.scopes_list = scopes_list
        self.index_exp = index_exp

class PrintStatement(AST):
    __doc__ = 'Representação de um comando de PRINT'
    def __init__(self):
        self.children = []

class PrintItem(AST):
    __doc__ = 'Representação de um item de PRINT'
    def __init__(self, token):
        self.token = token

class ReadStatement(AST):
    __doc__ = 'Representação do comando de leitura de dados via stdin'
    def __init__(self, dest_var):
        self.dest_var = dest_var

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

class ForStatement(AST):
    __doc__ = 'Representação de um FOR statement'
    def __init__(self, line_number, inside_assign, end_exp, step_exp, loop_statements, next_statement):
        self.line_number = line_number
        self.inside_assign = inside_assign
        self.end_exp = end_exp
        self.step_exp = step_exp
        self.loop_statements = loop_statements
        self.next_statement = next_statement

class NextStatement(AST):
    __doc__ = 'Representação de um NEXT statement'
    def __init__(self, line_number, scope_line, for_var):
        self.line_number = line_number
        self.scope_line = scope_line
        self.for_var = for_var

class DefStatement(AST):
    __doc__ = 'Representação de uma definição de funcao'
    def __init__(self, line_number, function_name, function_var, function_exp):
        self.line_number = line_number
        self.function_name = function_name
        self.function_var = function_var
        self.function_exp = function_exp

class FnCallStatement(AST):
    __doc__ = 'Representação de uma chamada de funcao'
    def __init__(self, function_name, function_exp):
        self.function_name = function_name
        self.function_exp = function_exp

class String(AST):
    __doc__ = 'Representação string'
    def __init__(self, value):
        self.value = value
        
class NoOp(AST):
    pass