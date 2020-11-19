from .token import *

class NodeVisitor(object):

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class CodeGenerator(NodeVisitor):
    VAR_DECLARATIONS = {"Global": {}}
    ARRAY_DECLARATIONS = {}
    FUNCTION_DEFINITIONS = {}
    STRING_DECLARATIONS = []

    generated_code = ''

    def __init__(self, parser):
        self.parser = parser

    def visit_Num(self, node):
        return f"${node.value}"

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == MINUS:
            return "$" + str(-1*int(self.visit(node.expr)[1:]))

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        print('BinOp', node.op.type, left, right)

        arr_preparation_code = ""

        # TODO: Adicionar tratamento de array multidimensinal
        # Arrays
        # # x
        # movl	_x, %edx

        # # y
        # movl	$13, %ecx 	# Dim2
        # imul	%ecx, %edx
        # movl	%edx, %eax

        # movl	_y, %edx
        # addl	%edx, %eax

        # # z
        # movl	$21, %ecx 	# Dim3
        # imul	%ecx, %edx
        # movl	%edx, %eax

        # movl	_z, %edx
        # addl	%edx, %eax

        if hasattr(node.left, "index_exp") and node.left.index_exp:
            # 1D
            if len(node.left.index_exp) == 1:
                print("BinOp LEFT - ARRAY - 1d")
                arr_preparation_code += f"\nmovl    {self.visit(node.left.index_exp[0])}, %ebx\n"
            # ND
            else:
                print("BinOp LEFT - ARRAY - Nd")
                for i, i_exp in enumerate(node.left.index_exp):
                    arr_preparation_code += f"\nmovl    {self.visit(i_exp)}, %edx\n\naddl	%edx, %eax\n"
                    if (i+1 < len(node.left.index_exp)):
                        cur_dim = self.ARRAY_DECLARATIONS[node.left.value][i+1]
                        arr_preparation_code += f"movl    ${cur_dim}, %ecx\n"
                        arr_preparation_code += f"imul    %ecx, %edx\n"
                        arr_preparation_code += f"movl    %edx, %eax\n"
                arr_preparation_code += f"movl\t$0, %ebx\naddl\t%eax, %ebx\n"
                
        elif hasattr(node.right, "index_exp") and node.right.index_exp:
            # 1D
            if len(node.right.index_exp) == 1:
                print("BinOp RIGHT - ARRAY - 1d")
                arr_preparation_code += f"\nmovl    {self.visit(node.right.index_exp[0])}, %ebx\n"
            # ND
            else:
                print("BinOp RIGHT - ARRAY - Nd")
                for i, i_exp in enumerate(node.right.index_exp):
                    arr_preparation_code += f"\nmovl    {self.visit(i_exp)}, %edx\n\naddl	%edx, %eax\n"
                    if (i+1 < len(node.right.index_exp)):
                        cur_dim = self.ARRAY_DECLARATIONS[node.right.value][i+1]
                        arr_preparation_code += f"movl    ${cur_dim}, %ecx\n"
                        arr_preparation_code += f"imul    %ecx, %edx\n"
                        arr_preparation_code += f"movl    %edx, %eax\n"
                arr_preparation_code += f"movl\t$0, %ebx\naddl\t%eax, %ebx\n"

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
            
            if hasattr(node.right, 'op'):
                result_code = op_2 + op_1 + opr
            else:
                result_code = op_1 + op_2 + opr


        return arr_preparation_code + result_code

    def visit_StatementList(self, node):
        child_code = []
        print(node.children)
        for child in node.children:
            if child.node.__class__.__name__ != "NoOp":
                line_number, visited = self.visit(child)
                child_code.append("\nlabel_" + str(line_number) + ":\nmovl\t$0, %eax\n" + visited)

        child_code = list(filter(lambda x: x != None, child_code))
        self.generated_code += ''.join(child_code)

    def visit_BaseStatement(self, node):
        return node.line_number, self.visit(node.node)

    def visit_Assign(self, node):
        print("visit_Assign")
        var_scopes_list = node.left.scopes_list
        var_name = node.left.value

        value = self.visit(node.right)
        
        # TODO: Adicionar tratamento para array multidimensional
        # Assign para arrays
        if node.left.index_exp is not None and node.left.value not in self.ARRAY_DECLARATIONS:
                raise NameError(f"Array: {node.left.value} não definido.")
        

        if node.left.value in self.ARRAY_DECLARATIONS:
            print("ASSIG ARRAY ASSIGN ARRAY")
            # Array 1D
            if len(node.left.index_exp) == 1: 
                print("ASSIGN - Array 1D")
                indexing_code = ""
        
                if node.left.index_exp[0].__class__.__name__ in ["Var"]:
                    indexing_code = f"movl   _{node.left.index_exp[0].value}, %ebx\n"
                elif node.left.index_exp[0].__class__.__name__ in ["BinOp"]:
                    indexing_code = f"{self.visit(node.left.index_exp[0])}\nmovl   %eax, %ebx\n"

                if hasattr(node.right, "index_exp") and node.right.index_exp:
                    if (len(node.right.index_exp) == 1):
                        return "TESTE movl\t" +  self.visit(node.right.index_exp) + f" ,%edx\n{indexing_code}movl\t%edx, " + self.visit(node.left) + "\n"
                    else:
                        return "movl\t" +  str(value) + f" ,%edx\n{indexing_code}movl\t%edx, " + self.visit(node.left) + "\n"
                elif node.right.__class__.__name__ in ["Var", "Num", "UnaryOp"]:
                    return "movl\t" +  str(value) + f" ,%edx\n{indexing_code}movl\t%edx, " + self.visit(node.left) + "\n"
                else:
                    return  str(value) + indexing_code + "movl\t" + "%eax" + ", " + self.visit(node.left) + "\n"
            # Array ND
            else: 
                print("ASSIGN - Array ND")
                indexing_code = ""

                for i, i_exp in enumerate(node.left.index_exp):
                    indexing_code += f"\nmovl    {self.visit(i_exp)}, %edx\n\naddl	%edx, %eax\n"
                    if (i+1 < len(node.left.index_exp)):
                        cur_dim = self.ARRAY_DECLARATIONS[node.left.value][i+1]
                        indexing_code += f"movl    ${cur_dim}, %ecx\n"
                        indexing_code += f"imul    %ecx, %edx\n"
                        indexing_code += f"movl    %edx, %eax\n"
                indexing_code += f"movl\t$0, %ebx\naddl\t%eax, %ebx\n"
        
                if hasattr(node.right, "index_exp") and node.right.index_exp:
                    if (len(node.right.index_exp) == 1):
                        return "movl\t" +  str(value) + " ,%edx\nmovl\t%edx, _" + var_name + "\n"
                    else:
                        right_index_code = ""
                        for i, i_exp in enumerate(node.right.index_exp):
                            right_index_code += f"\nmovl\t$0, %eax\nmovl    {self.visit(i_exp)}, %edx\n\naddl	%edx, %eax\n"
                            if (i+1 < len(node.right.index_exp)):
                                cur_dim = self.ARRAY_DECLARATIONS[node.right.value][i+1]
                                right_index_code += f"movl    ${cur_dim}, %ecx\n"
                                right_index_code += f"imul    %ecx, %edx\n"
                                right_index_code += f"movl    %edx, %eax\n"
                        right_index_code += f"movl\t$0, %ebx\naddl\t%eax, %ebx\n"
                        right_index_code += f"movl\t{value}, %eax\n"
                        return  indexing_code + "push\t%ebx\n\n" + right_index_code + "pop\t%ebx\nmovl\t" + "%eax" + ", " + self.visit(node.left) + "\n"
                if node.right.__class__.__name__ in ["Var", "Num", "UnaryOp"]:
                    return indexing_code + "\nmovl\t" +  str(value) + f" ,%edx\nmovl\t%edx, " + self.visit(node.left) + "\n"
                else:
                    return  indexing_code + "push\t%ebx\n\n" + str(value) + "pop\t%ebx\nmovl\t" + "%eax" + ", " + self.visit(node.left) + "\n"
                return "\nASSIGN - Array ND\n"

        # Assign para variaveis
        else:
            # Verifica o escopo
            if self.VAR_DECLARATIONS.get(var_scopes_list[-1]) is None:
                # adiciona escopo
                self.VAR_DECLARATIONS[var_scopes_list[-1]] = {}
                scope = self.VAR_DECLARATIONS[var_scopes_list[-1]]

            # Busca a variável no escopo atual e, caso falhe, nos escopos ateriores
            is_new_var = True
            for search_scope in var_scopes_list[::-1]:
                if self.VAR_DECLARATIONS[search_scope].get(var_name) is not None:
                    if search_scope != "Global":
                        var_name = var_name + "_" + search_scope
                    is_new_var = False
                    break
                
            if is_new_var:
                self.VAR_DECLARATIONS[var_scopes_list[-1]][var_name] = value
                if var_scopes_list[-1] != "Global":
                    var_name = var_name + "_" + var_scopes_list[-1]

            if hasattr(node.right, "index_exp"):
                if (len(node.right.index_exp) == 1):
                   return "movl\t" +  str(value) + " ,%edx\nmovl\t%edx, _" + var_name + "\n"
                else:
                    indexing_code = ""
                    for i, i_exp in enumerate(node.right.index_exp):
                        indexing_code += f"\nmovl    {self.visit(i_exp)}, %edx\n\naddl	%edx, %eax\n"
                        if (i+1 < len(node.right.index_exp)):
                            cur_dim = self.ARRAY_DECLARATIONS[node.right.value][i+1]
                            indexing_code += f"movl    ${cur_dim}, %ecx\n"
                            indexing_code += f"imul    %ecx, %edx\n"
                            indexing_code += f"movl    %edx, %eax\n"
                    indexing_code += f"movl\t$0, %ebx\naddl\t%eax, %ebx\n"
                    return indexing_code + "movl\t" +  str(value) + " ,%edx\nmovl\t%edx, _" + var_name + "\n"
            if node.right.__class__.__name__ in ["Var", "Num", "UnaryOp"]:
                return "movl\t" +  str(value) + " ,%edx\nmovl\t%edx, _" + var_name + "\n"
            else:
                return str(value) + "movl\t" + "%eax" + ", " + "_" + var_name + "\n"

    def visit_Var(self, node):
        var_name = node.value
        var_scope_line = node.scopes_list[-1]
        var_index_expressions = node.index_exp

        # Arrays
        if var_index_expressions:
            print("VAR INDEX EXP")
            print(var_index_expressions, var_name)
            if var_name not in self.ARRAY_DECLARATIONS:
                raise NameError(f"Array: {repr(var_name)} não definido.\nLinha {var_scope_line}.")
            
            # Array 1D
            if len(var_index_expressions) == 1: 
                if var_index_expressions[0].__class__.__name__ in ["Num", "UnaryOp"]:
                    var_name = var_name + f"+{var_index_expressions[0].value*4}"
                else:
                    var_name = var_name + f"(,%ebx,4)"
            # Array ND
            else:
                var_name = var_name + f"(,%ebx,4)"

            
            
            return "_" + str(var_name)

        # Variáveis normais
        else: 
            found_var = False
            for search_scope in node.scopes_list[::-1]:
                scope = self.VAR_DECLARATIONS.get(search_scope)
                if not scope:
                    continue
                if scope.get(var_name) is not None:
                    if search_scope != "Global":
                        var_name = var_name + "_" + search_scope
                    found_var = True
                    break
            
            # Verifica a variável
            if found_var == False:
                raise NameError(f"Variável: {repr(var_name)} não definida.\nLinha {var_scope_line}.")
            else:
                return "_" + str(var_name)
        
        
    def visit_NoOp(self, node):
        pass

    def visit_ReadStatement(self, node):
        print("VISIT READ STATEMENT")
        dest_var = node.dest_var
        print(dest_var)

        # Arrays
        if hasattr(dest_var, 'index_exp') and dest_var.index_exp:
            # 1D
            if len(dest_var.index_exp) == 1:
                if dest_var.value not in self.ARRAY_DECLARATIONS:
                    raise NameError(f"Array: {repr(dest_var.value)} não definido.")

                read_code = f"movl	{self.visit(node.dest_var.index_exp[0])}, %eax\nsall	$2, %eax\naddl	$_{dest_var.value}, %eax\nmovl  %eax, (%esp)\ncall _read\n"
                return read_code
            # ND
            else:
                indexing_code = "\nmovl\t$0, %eax\nmovl\t$0, %ebx\n"
                for i, i_exp in enumerate(node.dest_var.index_exp):
                    indexing_code += f"movl    {self.visit(i_exp)}, %edx\n\naddl	%edx, %eax\n"
                    if (i+1 < len(node.dest_var.index_exp)):
                        cur_dim = self.ARRAY_DECLARATIONS[node.dest_var.value][i+1]
                        indexing_code += f"movl    ${cur_dim}, %ecx\n"
                        indexing_code += f"imul    %ecx, %edx\n"
                        indexing_code += f"movl    %edx, %eax\n"
                indexing_code += f"movl\t$0, %ebx\naddl\t%eax, %ebx\nsall\t$2, %ebx\n"
                read_code = f"{indexing_code}addl	$_{node.dest_var.value}, %ebx\nmovl  %ebx, (%esp)\ncall _read\n"
                return read_code
        else: 
            dest_var_name = self.visit(dest_var)

            read_code = f"movl  ${dest_var_name}, (%esp)\ncall _read\n"

            return read_code

    def visit_PrintStatement(self, node):
        print("VISIT PRINT STATEMENT")
        child_code = []
        for child in node.children:
            if child.__class__.__name__ != "NoOp":
                child_code.append(self.visit(child))

        child_code = list(filter(lambda x: x != None, child_code))
        return '\n'.join(child_code)

    def visit_PrintItem(self, node):
        # Arrays
        if hasattr(node.token, 'index_exp') and node.token.index_exp:
            # 1D
            if len(node.token.index_exp) == 1:
                if node.token.index_exp[0].__class__.__name__ in ["Num", "UnaryOp"]:
                    read_code = f"movl\t_{node.token.value}+{node.token.index_exp[0].value*4}, %edx\nmovl\t%edx, (%esp)\ncall\t_print\nmovl\t$0, %eax"
                else:
                    if node.token.value not in self.ARRAY_DECLARATIONS:
                        raise NameError(f"Array: {node.token.value} não definido.")
                    read_code = f"movl	{self.visit(node.token.index_exp[0])}, %ebx\nmovl	_{node.token.value}(,%ebx, 4), %ebx\nmovl  %ebx, (%esp)\ncall _print\n"
                return read_code
            # ND
            else:
                indexing_code = "\nmovl\t$0, %eax\nmovl\t$0, %ebx\n"
                for i, i_exp in enumerate(node.token.index_exp):
                    indexing_code += f"movl    {self.visit(i_exp)}, %edx\n\naddl	%edx, %eax\n"
                    if (i+1 < len(node.token.index_exp)):
                        cur_dim = self.ARRAY_DECLARATIONS[node.token.value][i+1]
                        indexing_code += f"movl    ${cur_dim}, %ecx\n"
                        indexing_code += f"imul    %ecx, %edx\n"
                        indexing_code += f"movl    %edx, %eax\n"
                indexing_code += f"movl\t$0, %ebx\naddl\t%eax, %ebx\n"
                read_code = f"{indexing_code}movl	{self.visit(node.token)}, %ebx\nmovl  %ebx, (%esp)\ncall _print\n"
                return read_code
        # Strings
        elif node.token.__class__.__name__ == "String":
            # Verifica se string ja existe e, caso não exista, a insere na tabela de simbolos de strings
            string_value = node.token.value
            if string_value not in self.STRING_DECLARATIONS:
                self.STRING_DECLARATIONS.append(string_value)

            string_label = f"$_string_{self.STRING_DECLARATIONS.index(string_value)}"
            return f"movl\t{string_label},(%esp)\ncall\t_print_string\nmovl\t$0, %eax"
        else: 
            if node.token.__class__.__name__ in ["Var", "Num", "UnaryOp"]:
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

        # Adiciona a variável no escopo da funcao
        for_end_exp_var_name = f"for_{line_number}_end_exp"
        self.VAR_DECLARATIONS["Global"][for_end_exp_var_name] = "$0"

        end_exp_code = ""
        if end_exp.__class__.__name__ in ["Var", "Num", "UnaryOp"]:
            # end_exp_code = "movl\t" +  self.visit(end_exp) + " ,%ebx\n" + "movl	%ebx, (%esp)\n"
            end_exp_code = "movl\t" +  self.visit(end_exp) + f" ,_{for_end_exp_var_name}\n"
        else:
            # end_exp_code =  self.visit(end_exp) + "\nmovl\t" + "%eax ,%ebx\n" + "movl	%ebx, (%esp)\n"
            end_exp_code =  self.visit(end_exp) + "\nmovl\t" + f"%eax ,_{for_end_exp_var_name}\n"

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


        for_body_code += f"\nlabel_{next_statement.line_number}:\n\nmovl	{self.visit(next_statement.node.for_var)}, %eax\n"
        for_body_code += f"addl	{step_val}, %eax\n"
        for_body_code += f"movl	%eax, {self.visit(next_statement.node.for_var)}\n\n"

        for_control_code = f"for_{line_number}_control:\nmovl   {self.visit(next_statement.node.for_var)}, %eax\nmovl  _{for_end_exp_var_name}, %ebx\ncmpl	%ebx, %eax\njle	for_{line_number}_body"

        return for_assign_code + "\n" + for_body_code + "\n" + for_control_code + "\n"

    def visit_DefStatement(self, node):
        print("visit DefStatement")

        line_number = node.line_number
        function_name = node.function_name
        function_var = node.function_var
        function_exp = node.function_exp

        if function_name not in self.FUNCTION_DEFINITIONS.keys():
            self.FUNCTION_DEFINITIONS[function_name] = ""
        else:
            raise NameError(f"Tentativa de redefinição da função {repr(function_name)} na linha {line_number}")

        print("function_var")
        # Adiciona a variável no escopo da funcao
        self.VAR_DECLARATIONS[function_name] = {}
        self.VAR_DECLARATIONS[function_name][function_var.value] = "$0"

        def_code = f".globl fn_{function_name}\nfn_{function_name}:\n"
        def_code += f"movl	(%ebp), %eax\nmovl	%eax, {self.visit(function_var)}\n"

        def_code += self.visit(function_exp)

        def_code += "leave\nret\n"

        print("DEF CODE")
        print(def_code)
        self.FUNCTION_DEFINITIONS[function_name] = def_code
        return ""
        
    def visit_FnCallStatement(self, node):
        print("visit FnCallStatement")

        function_name = node.function_name
        function_exp = node.function_exp

        print(function_name)
        print(self.FUNCTION_DEFINITIONS)
        if function_name not in self.FUNCTION_DEFINITIONS.keys():
            raise NameError(f"Tentativa de chamada da função {repr(function_name)} não definida.")

        exp_code = ""
        if function_exp.__class__.__name__ in ["Num", "UnaryOp"]:
            exp_code += f"movl  {self.visit(function_exp)}, (%ebp)\n"
        elif function_exp.__class__.__name__ in ["Var"]:
            exp_code += f"movl {self.visit(function_exp)}, %eax\nmovl  %eax, (%ebp)\n"
        else:
            exp_code += f"{self.visit(function_exp)}\nmovl  %eax, (%ebp)\n"

        fn_call_code = f"{exp_code}\ncall   fn_{function_name}\n"

        return fn_call_code


    def visit_DimStatement(self, node):
        print("visit visit_DimStatement")

        array_var = node.arr_var
        array_dims = node.arr_dims

        self.ARRAY_DECLARATIONS[array_var.value] = array_dims

        return ""

    def generate(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        self.visit(tree)

        # Declaração de strings
        asm_code = "\t.section\t.rdata,\"dr\"\nLC0:\n.ascii\t\"%d\\12\\0\"\n"
        asm_code += "\nLC1:\n.ascii\t\"%d\\0\"\n"
        
        for i, decl_string in enumerate(self.STRING_DECLARATIONS):
            asm_code += f"_string_{i}:\n.ascii\t\"{decl_string}\\0\"\n"

        # Variaveis
        print("PROGRAM SCOPE")
        print(self.VAR_DECLARATIONS)
        asm_code += "\t.data\n\n"
        for scope in self.VAR_DECLARATIONS.keys():
            scope_suffix = ""
            if scope != "Global":
                scope_suffix = "_" + scope
            asm_code += '\n'.join(map(lambda k: f".comm	_{k}{scope_suffix}, 4, 4", self.VAR_DECLARATIONS[scope].keys())) + '\n'

        # Arrays
        for arr in self.ARRAY_DECLARATIONS.keys():
            arr_dims = self.ARRAY_DECLARATIONS[arr]
            arr_size = sum(arr_dims)*4
            asm_code += f".comm	_{arr}, {arr_size}, 2\n"

        
        # Código

        ## PRINT FUNCTION
        asm_code += "\n\n.text\n\n"
        asm_code += ".globl\t_print\n_print:\npushl\t%ebp\nmovl\t%esp, %ebp\nsubl\t$24, %esp\nmovl\t8(%ebp), %eax\nmovl\t%eax, 4(%esp)\nmovl\t$LC0, (%esp)\ncall	_printf\naddl	$24, %esp\nmovl	%ebp, %esp\nnop\nleave\nret\n\n"

        ## PRINT_STRING FUNCTION
        asm_code += ".globl	_print_string\n_print_string:\npushl	%ebp\nmovl	%esp, %ebp\nsubl	$24, %esp\nmovl	8(%ebp), %eax\nmovl	%eax, (%esp)\ncall	_puts\nnop\nleave\nret\n\n"

        ## SCAN FUNCTION
        asm_code += ".globl	_read\n_read:\npushl	%ebp\nmovl	%esp, %ebp\nsubl	$24, %esp\nmovl	8(%ebp), %eax\nmovl	%eax, 4(%esp)\nmovl	$LC1, (%esp)\ncall	_scanf\naddl	$24, %esp\nmovl	%ebp, %esp\nnop\nleave\nret\n\n"

        # Declaração de funções
        for fn_name in self.FUNCTION_DEFINITIONS:
            asm_code += self.FUNCTION_DEFINITIONS[fn_name]

        asm_code += "\n\n"

        asm_code += "\t.globl	_main\n_main:\npushl\t%ebp\nmovl\t%esp, %ebp\nandl\t$-16, %esp\nsubl\t$16, %esp\ncall	___main\n"
        asm_code += ''.join(list(map(lambda x: '\t' + x + '\n', self.generated_code.split('\n'))))

        asm_code += "\tleave\nret\n"

        return asm_code