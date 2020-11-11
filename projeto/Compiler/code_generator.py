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
    generated_code = ''

    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        print('BinOp', node.op.type, left, right)

        result_code = ""

        if node.op.type in [PLUS, MINUS]:
            op_1 = ""
            opr = ""
            op_2 = ""

            if node.op.type == PLUS:
                opr = "addl"
            if node.op.type == MINUS:
                opr = "subl"

            if not hasattr(node.left, 'op'):
                op_1 = "movl\t" + left + ", %edx\n" + opr + "\t%edx, %eax\n"
            elif hasattr(node.left, 'op'):
                op_1 = left + "\n"

            if not hasattr(node.right, 'op'):
                op_2 = opr + "\t" + right + ", %eax\n"
            elif hasattr(node.right, 'op'):
                op_2 = right + "\n"

            if hasattr(node.right, 'op') and node.right.op.type in [MUL, DIV, PLUS, MINUS]:
                result_code = op_2 + op_1
            else:
                result_code = op_1 + op_2

            if hasattr(node.right, 'op') and hasattr(node.left, 'op'):
                result_code = op_2 + "movl\t%eax, %ebx\n" + op_1 + opr + "\t%ebx, %eax\n"

            if not hasattr(node.right, 'op') and not hasattr(node.left, 'op'):
                result_code = "movl\t" + left + ", %eax\n" + "movl\t" + right + ",%edx\n" + opr + "\t%edx, %eax\n"

        else:
            op_1 = ""
            op_2 = ""
            opr = ""
            if node.op.type == MUL:
                opr = "imul\t%ecx, %edx\nmovl\t%edx, %eax\n"
            

                if not hasattr(node.left, 'op'):
                    op_1 = "movl\t" + left + ", %ecx\n"
                elif hasattr(node.left, 'op'):
                    op_1 = left + "\n" + "movl\t" + "%eax, %ecx\n"

                if not hasattr(node.right, 'op'):
                    op_2 = "movl\t" + right + ", %edx\n"
                elif hasattr(node.right, 'op'):
                    op_2 = right + "\n" + "movl\t" + "%eax, %edx\n"
                    
            elif node.op.type == DIV:
                opr = "movl\t$0, %edx\nidiv\t%ecx\n"

                if not hasattr(node.left, 'op'):
                    op_1 = "movl\t" + left + ", %eax\n"
                elif hasattr(node.left, 'op'):
                    op_1 = left + "\n"

                if not hasattr(node.right, 'op'):
                    op_2 = "movl\t" + right + ", %ecx\n"
                elif hasattr(node.right, 'op'):
                    op_2 = right + "\n" + "movl\t" + "%eax, %ecx\n"

            result_code = op_1 + op_2 + opr


        return result_code



    def visit_Num(self, node):
        return f"${node.value}"

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return str(int(self.visit(node.expr)))
        if op == MINUS:
            return "$" + str(-1*int(self.visit(node.expr)[1:]))

    def visit_StatementList(self, node):
        child_code = []
        for child in node.children:
            if child.__class__.__name__ != "NoOp":
                child_code.append("\nmovl\t$0, %eax\n" + self.visit(child))

        child_code = list(filter(lambda x: x != None, child_code))
        self.generated_code += ''.join(child_code)

    def visit_Assign(self, node):
        var_name = node.left.value
        value = self.visit(node.right)
        self.GLOBAL_SCOPE[var_name] = value

        if node.right.__class__.__name__ in ["Var", "Num", "UnaryOp"]:
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

    def visit_PrintStatement(self, node):
        print("VISIT PRINT STATEMENT")
        child_code = []
        for child in node.children:
            if child.__class__.__name__ != "NoOp":
                child_code.append(self.visit(child))

        child_code = list(filter(lambda x: x != None, child_code))
        return '\n'.join(child_code)

    def visit_PrintItem(self, node):
        if node.token.__class__.__name__ in ["Var", "Num"]:
            val = self.visit(node.token)
            return f"movl\t{val}, %edx\nmovl\t%edx, (%esp)\ncall\t_print\nmovl\t$0, %eax"
        else:
            exp = self.visit(node.token)
            return f"\n{exp}\nmovl\t%eax, %edx\nmovl\t%edx, (%esp)\ncall\t_print\nmovl\t$0, %eax"

    def visit_IfStatement(self, node):
        print("Visit IfStatement")
        left_exp = node.left_exp
        operator = node.operator
        right_exp = node.right_exp
        line = node.line
        print(left_exp)
        print(operator)
        print(right_exp)
        print(line)

    def generate(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        self.visit(tree)

        # prinf
        asm_code = "\t.section\t.rdata,\"dr\"\nLC0:\n.ascii\t\"%d\\12\\0\"\n"

        # Variaveis
        asm_code += "\t.data\n\n"
        asm_code += '\n'.join(map(lambda k: f".comm	_{k}, 4, 4", self.GLOBAL_SCOPE.keys())) + '\n'

        # Código
        asm_code += "\n\n.text\n\n"
        asm_code += ".globl\t_print\n_print:\npushl\t%ebp\nmovl\t%esp, %ebp\nsubl\t$24, %esp\nmovl\t8(%ebp), %eax\nmovl\t%eax, 4(%esp)\nmovl\t$LC0, (%esp)\ncall	_printf\nnop\nleave\nret\n\n"

        asm_code += "\t.globl	_main\n_main:\npushl\t%ebp\nmovl\t%esp, %ebp\nandl\t$-16, %esp\nsubl\t$16, %esp\ncall	___main\n"
        asm_code += ''.join(list(map(lambda x: '\t' + x + '\n', self.generated_code.split('\n'))))

        asm_code += "\tleave\nret\n"

        return asm_code