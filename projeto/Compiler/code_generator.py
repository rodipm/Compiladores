from .token import *

class NodeVisitor(object):

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class CodeGenerator(NodeVisitor):
    GLOBAL_SCOPE = {}
    NUMERIC_CONSTANS = {}
    generated_code = ''
    code_obj = ''

    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            left = self.visit(node.left)
            right = self.visit(node.right)
            print('BinOp', node.op.type, left, right)
            if hasattr(node.right, 'op'):
                if node.right.op.type in [MUL, DIV, PLUS, MINUS]:
                    print('inverted')
                    return right + '+ ' + left
            return left + '+ ' + right
        if node.op.type == MINUS:
            left = self.visit(node.left)
            right = self.visit(node.right)
            print('BinOp', node.op.type, left, right)
            left = self.visit(node.left)
            right = self.visit(node.right)
            print('BinOp', node.op.type, left, right)
            if hasattr(node.right, 'op'):
                if node.right.op.type in [MUL, DIV, PLUS, MINUS]:
                    print('inverted')
                    return right + '- ' + left
            return left + '- ' + right
        if node.op.type == MUL:
            left = self.visit(node.left)
            right = self.visit(node.right)
            print('BinOp', node.op.type, left, right)
            if hasattr(node.right, 'op'):
                if node.right.op.type in [MUL, DIV, PLUS, MINUS]:
                    print('inverted')
                    return right + '* ' + left
            return left + '* ' + right
        if node.op.type == DIV:
            left = self.visit(node.left)
            right = self.visit(node.right)
            print('BinOp', node.op.type, left, right)
            if hasattr(node.right, 'op'):
                if node.right.op.type in [MUL, DIV, PLUS, MINUS]:
                    print('inverted')
                    return right + '/ ' + left
            return left + '/ ' + right


    def visit_Num(self, node):
        num_const_label = f"N{node.value}"
        hex_value = '/' + hex(node.value)[2:].zfill(2)
        if num_const_label not in self.NUMERIC_CONSTANS.keys():
            self.NUMERIC_CONSTANS[num_const_label] = f"{num_const_label}\tK\t{hex_value}"
        return num_const_label + '\n'

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        if op == MINUS:
            return -self.visit(node.expr)

    def visit_StatementList(self, node):
        child_code = []
        for child in node.children:
            child_code.append(self.visit(child))

        child_code = list(filter(lambda x: x != None, child_code))
        self.generated_code += ''.join(child_code)

    def visit_Assign(self, node):
        var_name = node.left.value
        value = self.visit(node.right)
        self.GLOBAL_SCOPE[var_name] = value
        return 'LD ' + str(value) + 'MM ' + var_name + '\n'

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return str(var_name) + '\n'

    def visit_NoOp(self, node):
        pass

    def generate(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        self.visit(tree)
        asm_code = 'INICIO\t@\t/0100\n'
        asm_code += ''.join(list(map(lambda x: '\t' + x + '\n', self.generated_code.split('\n'))))
        asm_code += '\tCN\t/00\n\t@\t/0500\t;Dados\n'
        asm_code += '\n'.join(map(lambda k: f"{k}\tK\t/00", self.GLOBAL_SCOPE.keys())) + '\n'
        asm_code += '\n'.join(self.NUMERIC_CONSTANS.values())
        return asm_code