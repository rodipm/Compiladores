from .ast import *
from .token import *

class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.scopes = ["Global"]
        self.line_number = ""

    def enter_scope(self, line_number):
        self.scopes.append(str(line_number))

    def exit_scope(self):
        if self.current_scope() != "Global":
            self.scopes = self.scopes[:-1]

    def current_scope(self):
        return self.scopes[-1]


    def error(self, expected):
        raise Exception(f'Sintaxe inválida na linha:{self.line_number}.\nTipo de Token Esperado: {expected}.\nToken Encontrado: {self.current_token}')

    def consome(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type)

    
    def empty(self):
        """An empty production"""
        return NoOp()

    def Program(self):
        """
         Program : BStatement BStatement*
        """
        print("(Program)")
        node = self.BStatement()

        nodes = [node]

        while self.current_token.type == INTEGER:
            nodes.append(self.BStatement())

        root = StatementList()
        for node in nodes:
            root.children.append(node)

        return root

    def BStatement(self):
        """
            BStatement : INTEGER Assign | PRINT | IF | FOR | NEXT | GOTO | DEF | READ | DIM | Remark 
        """
        print("(BStatement)")
        node = None
        print(self.current_token)
        line_number = self.current_token.value
        self.line_number = line_number
        print("Line Number: ", line_number)

        self.consome(INTEGER)
        print("->INTEGER->")

        if self.current_token.type == LET:
            node = self.Assign()
        elif self.current_token.type == GOTO or self.current_token.type == GO:
            node = self.Goto()
        elif self.current_token.type == REM:
            node = self.Remark()
        elif self.current_token.type == IF:
            node = self.If()
        elif self.current_token.type == FOR:
            node = self.For(line_number)
        elif self.current_token.type == NEXT:
            node = self.Next(line_number)
        elif self.current_token.type == PRINT:
            node = self.Print()
        elif self.current_token.type == READ:
            node = self.Read()
        elif self.current_token.type == DIM:
            node = self.Dim()
        elif self.current_token.type == DEF:
            node = self.Def(line_number)

        base_statement = BaseStatement(line_number, node)

        return base_statement

    def Assign(self):
        """
            Assign : LET Var EQUAL Exp
        """
        print("(Assign)")
        self.consome(LET)
        print("->LET->")
        left = self.Var()

        token = self.current_token
        self.consome(EQUAL)
        print("->EQUAL->")

        right = self.Exp()

        node = Assign(left, token, right)
        return node

    def Var(self):
        """
           Var : ID | ID [Exp (, Exp)*]
        """
        print("(Var)")
        cur_token = self.current_token
        self.consome(ID)
        print("->ID->")

        index_exp = []
        if self.current_token.type == OPENBRACKET:
            print("(OPENBRACKET)")
            self.consome(OPENBRACKET)

            index_exp.append(self.Exp())

            while self.current_token.type == COMMA:
                print("(COMMA)")
                sellf.consome(COMMA)

                index_exp.append(self.Exp())
            
            print("(CLOSEBRACKET)")
            self.consome(CLOSEBRACKET)

        if len(index_exp) == 0:
            index_exp = None

        return Var(cur_token, self.scopes[:], index_exp)

    def Exp(self):
        """
            Exp: Term (PLUS|MINUS Term)*
        """
        print("(Exp)")
        node = self.Term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.consome(PLUS)
                print("->PLUS->")
            else:
                if token.type == MINUS:
                    self.consome(MINUS)
                    print("->MINUS->")
            node = BinOp(left=node, op=token, right=(self.Term()))

        return node

    def Term(self):
        """
            Term: Eb ((MUL | DIV) Eb)*
        """
        print("(Term)")
        node = self.Eb()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.consome(MUL)
                print("->MUL->")
            else:
                if token.type == DIV:
                    self.consome(DIV)
                    print("->DIV->")
            node = BinOp(left=node, op=token, right=(self.Eb()))

        return node

    def Read(self):
        """
            Read : READ Var
        """
        print("(READ)")
        self.consome(READ)

        read_var = self.Var()
        return ReadStatement(read_var)

    def Print(self):
        """
            Print : PRINT Pitem (COMMA Pitem)* | (COMMA Pitem)* COMMA
        """
        print("Print")
        self.consome(PRINT)

        print_root = PrintStatement()

        print_root.children.append(self.Pitem())

        token = self.current_token
        print("AFTER FIRST PITEM")
        print("TOKEN: ", token)

        while token.type == COMMA:
            print("Eating comma")
            self.consome(COMMA)
            print_root.children.append(self.Pitem())
            token = self.current_token
        
        return print_root

    def Pitem(self):
        """
            Pitem : Exp | STRING
        """
        print("(Pitem)")
        print(self.current_token.type)
        if self.current_token.type == STRING:
            print("IS STRING")
            string_node = self.current_token
            self.consome(STRING)
            return PrintItem(String(string_node.value))
        else:
            return PrintItem(self.Exp())


    def Eb(self):
        """
            Eb : PLUS Eb
                  | MINUS Eb
                  | INTEGER
                  | LPAREN Exp RPAREN
                  | Var
                  | FN ID LPAREN Exp RPAREN
        """
        print("(Eb)")
        token = self.current_token
        if token.type == PLUS:
            self.consome(PLUS)
            print("->PLUS->")
            node = UnaryOp(token, self.Eb())
            return node
        if token.type == MINUS:
            self.consome(MINUS)
            print("->MINUS->")
            node = UnaryOp(token, self.Eb())
            return node
        if token.type == INTEGER:
            self.consome(INTEGER)
            print("->INTEGER->")
            return Num(token)
        if token.type == LPAREN:
            self.consome(LPAREN)
            print("->LPAREN->")
            node = self.Exp()
            self.consome(RPAREN)
            print("->RPAREN->")
            return node
        if token.type == FN:
            print("(FN)")
            self.consome(FN)

            function_name = self.current_token.value
            self.consome(ID)
            print("FUNCTION NAME FN CALL")
            print(function_name)

            self.consome(LPAREN)
            print("->LPAREN->")

            function_exp = self.Exp()

            self.consome(RPAREN)
            print("->RPAREN->")
            return FnCallStatement(function_name, function_exp)

        node = self.Var()
        return node

    def Goto(self):
        """
            Goto : (GOTO | GO TO) Integer
        """
        print("Goto")
        token = self.current_token
        print(token)
        if token.type == GOTO:
            self.consome(GOTO)
            print("(GOTO)")

        elif token.type == GO:
            self.consome(GO)
            print("(GO)")
            self.consome(TO)
            print("(TO)")

        integer_token = self.current_token
        self.consome(INTEGER)
        print("->INTEGER->")

        return GotoStatement(integer_token.value)

    def If(self):
        """
            If : IF Exp (EQ | NOTEQ | GT | LESS | GTEQ | LESSEQ) Exp THEN INTEGER
        """
        print("(IF)")
        self.consome(IF)
        left_exp = self.Exp()

        token = self.current_token
        operator = None
        if token.type == EQ:
            self.consome(EQ)
            print("IS EQ")
        elif token.type == NOTEQ:
            self.consome(NOTEQ)
            print("IS NOTEQ")
        elif token.type == GT:
            self.consome(GT)
            print("IS GT")
        elif token.type == LESS:
            self.consome(LESS)
            print("IS LESS")
        elif token.type == GTEQ:
            self.consome(GTEQ)
            print("IS GTEQ")
        elif token.type == LESSEQ:
            self.consome(LESSEQ)
            print("IS LESSEQ")

        operator = token
        print("OPERATOR = ", operator)

        right_exp = self.Exp()

        self.consome(THEN)

        token = self.current_token

        destination_line = None
        if token.type == INTEGER:
            destination_line = token.value
            self.consome(INTEGER)
        
        return IfStatement(left_exp, operator, right_exp, destination_line)

    def For(self, line_number):
        """
            For : (FOR VAR EQUAL Exp TO Exp | FOR ID EQUAL Exp TO Exp STEP Exp) BStatement* INT NEXT VAR
        """
        self.enter_scope(line_number)

        print("(FOR)")
        self.consome(FOR)

        print("(VAR)")
        for_var = self.Var()

        print("(EQUAL)")
        for_assign_token = self.current_token
        self.consome(EQUAL)

        print("(EXP)")
        assign_exp = self.Exp()

        inside_assign = Assign(for_var, for_assign_token, assign_exp)

        print("(TO)")
        self.consome(TO)

        print("(EXP)")
        end_exp = self.Exp()

        step_exp = None

        if self.current_token.type == "STEP":
            print("(STEP)")
            self.consome(STEP)

            step_exp = self.Exp()

        loop_statements = StatementList()
        cur_statement = None
        while self.current_token.type == INTEGER:
            cur_statement = self.BStatement()
            if cur_statement.node.__class__.__name__ == "NextStatement":
                break
            loop_statements.children.append(cur_statement)

        next_statement = cur_statement

        print("LOOP STATEMENTS")
        print(loop_statements)
        return ForStatement(line_number, inside_assign, end_exp, step_exp, loop_statements, next_statement)

    def Next(self, line_number):
        """
            Next : NEXT VAR
        """
        print("(NEXT)")
        self.consome(NEXT)
        for_var = self.Var()

        current_scope_line = self.current_scope()
        self.exit_scope()
        return NextStatement(line_number, current_scope_line, for_var)

    def Def(self, line_number):
        """
            Def : DEF FN ID LPAREN Var RPAREN EQUAL Exp
        """

        print("(DEF)")
        self.consome(DEF)

        print("(FN)")
        print(self.current_token)
        self.consome(FN)

        function_name = self.current_token.value
        self.enter_scope(function_name)


        print(self.current_token)
        print("(ID)")
        self.consome(ID)

        print("(LPAREN)")
        self.consome(LPAREN)

        print("(VAR)")
        function_var = self.Var()

        print("(RPAREN)")
        self.consome(RPAREN)
        
        print("(EQUAL)")
        self.consome(EQUAL)

        function_exp = self.Exp()

        self.exit_scope()

        return DefStatement(line_number, function_name, function_var, function_exp)

    def Remark(self):
        """
            Remark : REM STRING
        """
        self.consome(REM)
        self.consome(STRING)
        return self.empty()

    def Dim(self):
        """
            Dim : DIM ID LPAREN INTEGER (COMMA INTEGER)* RPAREN
        """

        print("(DIM)")
        self.consome(DIM)

        array_var = self.Var()

        print("(LPAREN)")
        self.consome(LPAREN)
        
        array_dims = []
        array_dims.append(self.current_token.value)

        print("(INTEGER)")
        self.consome(INTEGER)
    	
        while self.current_token.type == COMMA:
            self.consome(COMMA)

            array_dims.append(self.current_token.value)
        
            print("(INTEGER)")
            self.consome(INTEGER)

        print("(RPAREN)")
        self.consome(RPAREN)

        return  DimStatement(array_var, array_dims)

    def Return(self):
        """
        Return : RETURN
        """
        pass
        
    def parse(self):
        """
            Program : BStatement BStatement*

            BStatement : INTEGER Assign | PRINT | GOTO | IF | FOR | NEXT | DEF | REMARK | END

            Assign : LET Var = Exp

            Var : ID | ID [Exp (, Exp)*]

            Exp: Term (PLUS|MINUS Term)*

            Term: Eb ((MUL | DIV) Eb)*

            Eb: PLUS Eb | MINUS Eb | INTEGER | LPAREN Exp RPAREN | INTEGER | Var | FN letter LPAREN Exp RPAREN

            Read : READ Var

            Print : PRINT Pitem (COMMA Pitem)* | (COMMA Pitem)* COMMA

            Pitem : Exp | STRING

            Goto : (GOTO | GO TO) Integer
            
            If : IF Exp (EQ | NOTEQ | GT | LESS | GTEQ | LESSEQ) Exp THEN INTEGER
            
            For : (FOR VAR EQUAL Exp TO Exp | FOR VAR EQUAL Exp TO Exp STEP Exp) BStatement* NEXT VAR

            Def : DEF FN ID LPAREN ID RPAREN EQUAL Exp

            Dim : DIM ID LPAREN INTEGER (COMMA INTEGER)* RPAREN (COMMA ID LPAREN INTEGER (COMMA INTEGER)* RPAREN) *
            
            Return: RETURN

            Remark : REM STRING
        """
        print("*****************PARSE***********************")
        node = self.Program()
        if self.current_token.type != EOF:
            self.error(EOF)
        print("*****************END PARSE***********************")
        return node