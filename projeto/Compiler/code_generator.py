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
        left = self.visit(node.left)
        right = self.visit(node.right)

        print('BinOp', node.op.type, left, right)

        result_code = ""

        if node.op.type in [PLUS, MINUS]:
            left_code = ""
            mid_op = ""
            right_code = ""

            if node.op.type == PLUS:
                mid_op = "addl"
            if node.op.type == MINUS:
                mid_op = "subl"

            if not hasattr(node.left, 'op'):
                left_code = "movl\t" + left + ", %edx\n" + mid_op + "\t%edx, %eax\n"
            elif hasattr(node.left, 'op'):
                left_code = left + "\n"

            if not hasattr(node.right, 'op'):
                right_code = mid_op + "\t" + right + ", %eax\n"
            elif hasattr(node.right, 'op'):
                right_code = right + "\n"

            result_code = right_code + left_code 

        else:
            op_1 = ""
            op_2 = ""
            opr = ""
            if node.op.type == MUL:
                opr = "imul\t%ecx, %edx\nmovl\t%edx, %eax\n"
            if node.op.type == DIV:
                opr = "subl"

            if not hasattr(node.left, 'op'):
                op_1 = "movl\t" + left + ", %ecx\n"
            elif hasattr(node.left, 'op'):
                op_1 = left + "\n" + "movl\t" + "%eax, %ecx\n"

            if not hasattr(node.right, 'op'):
                op_2 = "movl\t" + right + ", %edx\n"
            elif hasattr(node.right, 'op'):
                op_2 = left + "\n" + "movl\t" + "%eax, %edx\n"

            result_code = op_1 + op_2 + opr


        return result_code



    def visit_Num(self, node):
        return f"${node.value}"

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        if op == MINUS:
            return -self.visit(node.expr)

    def visit_StatementList(self, node):
        child_code = []
        for child in node.children:
            child_code.append("\nmovl\t$0, %eax\n" + self.visit(child))

        child_code = list(filter(lambda x: x != None, child_code))
        self.generated_code += ''.join(child_code)

    def visit_Assign(self, node):
        var_name = node.left.value
        value = self.visit(node.right)
        self.GLOBAL_SCOPE[var_name] = value

        if node.right.__class__.__name__ in ["Var", "Num"]:
            return "movl\t" +  str(value) + " ,%edx\nmovl\t%edx, _" + var_name + "\n"
        else:
            return str(value) + "movl\t" + "%eax" + ", " + "_" + var_name + "\n"

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return "_" + str(var_name)

    def visit_NoOp(self, node):
        pass

    def generate(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        self.visit(tree)

        # Variaveis
        asm_code = "\t.data\n\n"
        asm_code += '\n'.join(map(lambda k: f".comm	_{k}, 4, 4", self.GLOBAL_SCOPE.keys())) + '\n'

        # Código
        asm_code += "\n\n.text\n\n"
        asm_code += "\t.globl	_main\n_main:\n"

        # asm_code += "\tmovl\t$0, %eax\n"
        asm_code += ''.join(list(map(lambda x: '\t' + x + '\n', self.generated_code.split('\n'))))

        asm_code += "\tret\n"

        return asm_code