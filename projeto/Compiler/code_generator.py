from .token import *

class NodeVisitor(object):

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class CodeGenerator(NodeVisitor):
    PROGRAM_SCOPE = {"Global": {}}
    generated_code = ''

    def __init__(self, parser):
        self.parser = parser

    def visit_Num(self, node):
        return f"${node.value}"

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return str(int(self.visit(node.expr)))
        if op == MINUS:
            return "$" + str(-1*int(self.visit(node.expr)[1:]))

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

    def visit_StatementList(self, node):
        child_code = []
        for child in node.children:
            if child.__class__.__name__ != "NoOp":
                line_number, visited = self.visit(child)
                child_code.append("\nlabel_" + str(line_number) + ":\nmovl\t$0, %eax\n" + visited)

        child_code = list(filter(lambda x: x != None, child_code))
        self.generated_code += ''.join(child_code)

    def visit_BaseStatement(self, node):
        return node.line_number, self.visit(node.node)

    def visit_Assign(self, node):
        print("Visit Assign")

        var_name = node.left.value
        var_scopes_list = node.left.scopes_list

        value = self.visit(node.right)
        
        print(var_name, var_scopes_list, value)
        # Verifica o escopo
        if self.PROGRAM_SCOPE.get(var_scopes_list[-1]) is None:
            # adiciona escopo
            self.PROGRAM_SCOPE[var_scopes_list[-1]] = {}
            scope = self.PROGRAM_SCOPE[var_scopes_list[-1]]

        # Busca a variável no escopo atual e, caso falhe, nos escopos ateriores
        is_new_var = True
        for search_scope in var_scopes_list[::-1]:
            if self.PROGRAM_SCOPE[search_scope].get(var_name) is not None:
                if search_scope != "Global":
                    var_name = var_name + "_" + search_scope
                is_new_var = False
                break
            
        if is_new_var:
            self.PROGRAM_SCOPE[var_scopes_list[-1]][var_name] = value
            if var_scopes_list[-1] != "Global":
                var_name = var_name + "_" + var_scopes_list[-1]

        if node.right.__class__.__name__ in ["Var", "Num", "UnaryOp"]:
            return "movl\t" +  str(value) + " ,%edx\nmovl\t%edx, _" + var_name + "\n"
        else:
            return str(value) + "movl\t" + "%eax" + ", " + "_" + var_name + "\n"

    def visit_Var(self, node):
        print("VISIT VAR")
        var_name = node.value
        var_scope_line = node.scopes_list[-1]

        found_var = False
        for search_scope in node.scopes_list[::-1]:
            scope = self.PROGRAM_SCOPE.get(search_scope)
            if not scope:
                continue
            if scope.get(var_name) is not None:
                if search_scope != "Global":
                    var_name = var_name + "_" + search_scope
                found_var = True
                break
        
        # Verifica a variável
        if found_var == False:
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

    def visit_GotoStatement(self, node):
        label_name = "label_" + str(node.destination_line)
        return f"jmp {label_name}\n"

    def visit_IfStatement(self, node):
        print("Visit IfStatement")
        left_exp = node.left_exp
        operator = node.operator
        right_exp = node.right_exp
        destination_line = node.destination_line

        expressions_code = ""

        left_val = self.visit(left_exp)
        right_val = self.visit(right_exp)

        if (left_exp.__class__.__name__ in ["Num", "Var"]):
            expressions_code += f"movl  {left_val}, %ecx\n"
        else:
            expressions_code += f"{left_val} movl %eax, %ecx\n"
            

        if (right_exp.__class__.__name__ in ["Num", "Var"]):
            expressions_code += f"movl	{right_val}, %edx\n"
        else:
            expressions_code += f"{right_val}movl %eax, %edx\n"

        conditional_type_code = ""

        if operator.type == EQ:
            conditional_type = "je"
        elif operator.type == NOTEQ:
            conditional_type = "jne"
        elif operator.type == GT:
            conditional_type = "jg"
        elif operator.type == LESS:
            conditional_type = "jl"
        elif operator.type == GTEQ: 
            conditional_type = "jge"
        elif operator.type == LESSEQ:
            conditional_type = "jle"

        destination_label = f"label_{destination_line}"

        expressions_code += f"cmpl  %edx, %ecx\n"
        expressions_code += f"{conditional_type}    {destination_label}\n"

        print(left_exp)
        print(operator)
        print(right_exp)
        print(destination_line)
        print(expressions_code)
        return expressions_code

    def visit_ForStatement(self, node):
        print("visit ForStatement")

        line_number = node.line_number
        inside_assign = node.inside_assign
        end_exp = node.end_exp
        step_exp = node.step_exp
        loop_statements = node.loop_statements
        next_statement = node.next_statement

        end_exp_code = ""
        if end_exp.__class__.__name__ in ["Var", "Num", "UnaryOp"]:
            end_exp_code = "movl\t" +  self.visit(end_exp) + " ,%ebx\n" + "movl	%ebx, (%esp)\n"
        else:
            end_exp_code =  self.visit(end_exp) + "\nmovl\t" + "%eax ,%ebx\n" + "movl	%ebx, (%esp)\n"

        for_assign_code = self.visit(inside_assign)
        for_assign_code += f"{end_exp_code}\njmp for_{line_number}_control\n"

        for_body_code = f"for_{line_number}_body:\n"
        if loop_statements:
            for b_statement in loop_statements.children:
                loop_line_number, visited = self.visit(b_statement)
                for_body_code += "\nlabel_" + str(loop_line_number) + ":\nmovl\t$0, %eax\n" + visited

        step_val = "$1"
        if step_exp:
            step_val = self.visit(step_exp)



        for_body_code += f"\n\nmovl	{self.visit(next_statement.node.for_var)}, %eax\n"
        for_body_code += f"addl	{step_val}, %eax\n"
        for_body_code += f"movl	%eax, {self.visit(next_statement.node.for_var)}\n\n"

        for_control_code = f"for_{line_number}_control:\nmovl   {self.visit(next_statement.node.for_var)}, %eax\nmovl  (%esp), %ebx\ncmpl	%ebx, %eax\njle	for_{line_number}_body"

        return for_assign_code + "\n" + for_body_code + "\n" + for_control_code + "\n"

    def generate(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        self.visit(tree)

        # prinf
        asm_code = "\t.section\t.rdata,\"dr\"\nLC0:\n.ascii\t\"%d\\12\\0\"\n"

        # Variaveis
        asm_code += "\t.data\n\n"
        for scope in self.PROGRAM_SCOPE.keys():
            scope_suffix = ""
            if scope != "Global":
                scope_suffix = "_" + scope
            asm_code += '\n'.join(map(lambda k: f".comm	_{k}{scope_suffix}, 4, 4", self.PROGRAM_SCOPE[scope].keys())) + '\n'

        # Código
        asm_code += "\n\n.text\n\n"
        asm_code += ".globl\t_print\n_print:\npushl\t%ebp\nmovl\t%esp, %ebp\nsubl\t$24, %esp\nmovl\t8(%ebp), %eax\nmovl\t%eax, 4(%esp)\nmovl\t$LC0, (%esp)\ncall	_printf\nnop\nleave\nret\n\n"

        asm_code += "\t.globl	_main\n_main:\npushl\t%ebp\nmovl\t%esp, %ebp\nandl\t$-16, %esp\nsubl\t$16, %esp\ncall	___main\n"
        asm_code += ''.join(list(map(lambda x: '\t' + x + '\n', self.generated_code.split('\n'))))

        asm_code += "\tleave\nret\n"

        return asm_code