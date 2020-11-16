from .ast import *
from .token import *

class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.scopes = ["Global"]

    def enter_scope(self, line_number):
        self.scopes.append(str(line_number))

    def exit_scope(self):
        if self.current_scope() != "Global":
            self.scopes = self.scopes[:-1]

    def current_scope(self):
        return self.scopes[-1]


    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    
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
            BStatement : INTEGER Assign | PRINT | IF | FOR | NEXT | GOTO | Remark 
        """
        print("(BStatement)")
        node = None
        print(self.current_token)
        line_number = self.current_token.value
        print("Line Number: ", line_number)

        self.eat(INTEGER)
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

        base_statement = BaseStatement(line_number, node)

        return base_statement

    def Assign(self):
        """
            Assign : LET Var EQUAL Exp
        """
        print("(Assign)")
        self.eat(LET)
        print("->LET->")
        left = self.Var()

        token = self.current_token
        self.eat(EQUAL)
        print("->EQUAL->")

        right = self.Exp()

        node = Assign(left, token, right)
        return node

    def Var(self):
        """
            Var : ID
        """
        print("(Var)")
        node = Var(self.current_token, self.scopes[:])
        self.eat(ID)
        print("->ID->")
        return node

    def Exp(self):
        """
            Exp: Term (PLUS|MINUS Term)*
        """
        print("(Exp)")
        node = self.Term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                print("->PLUS->")
            else:
                if token.type == MINUS:
                    self.eat(MINUS)
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
                self.eat(MUL)
                print("->MUL->")
            else:
                if token.type == DIV:
                    self.eat(DIV)
                    print("->DIV->")
            node = BinOp(left=node, op=token, right=(self.Eb()))

        return node

    def Print(self):
        """
            Print : PRINT Pitem (COMMA Pitem)* | (COMMA Pitem)* COMMA
        """
        print("Print")
        self.eat(PRINT)

        print_root = PrintStatement()

        print_root.children.append(self.Pitem())

        token = self.current_token
        print("AFTER FIRST PITEM")
        print("TOKEN: ", token)

        while token.type == COMMA:
            print("Eating comma")
            self.eat(COMMA)
            print_root.children.append(self.Pitem())
            token = self.current_token
        
        return print_root

    def Pitem(self):
        """
            Pitem : Exp
        """
        print("(Pitem)")
        
        return PrintItem(self.Exp())

    def Eb(self):
        """
            Eb : PLUS Eb
                  | MINUS Eb
                  | INTEGER
                  | LPAREN Exp RPAREN
                  | Var
        """
        print("(Eb)")
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            print("->PLUS->")
            node = UnaryOp(token, self.Eb())
            return node
        if token.type == MINUS:
            self.eat(MINUS)
            print("->MINUS->")
            node = UnaryOp(token, self.Eb())
            return node
        if token.type == INTEGER:
            self.eat(INTEGER)
            print("->INTEGER->")
            return Num(token)
        if token.type == LPAREN:
            self.eat(LPAREN)
            print("->LPAREN->")
            node = self.Exp()
            self.eat(RPAREN)
            print("->RPAREN->")
            return node
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
            self.eat(GOTO)
            print("(GOTO)")

        elif token.type == GO:
            self.eat(GO)
            print("(GO)")
            self.eat(TO)
            print("(TO)")

        integer_token = self.current_token
        self.eat(INTEGER)
        print("->INTEGER->")

        return GotoStatement(integer_token.value)

    def If(self):
        """
            If : IF Exp (EQ | NOTEQ | GT | LESS | GTEQ | LESSEQ) Exp THEN INTEGER
        """
        print("(IF)")
        self.eat(IF)
        left_exp = self.Exp()

        token = self.current_token
        operator = None
        if token.type == EQ:
            self.eat(EQ)
            print("IS EQ")
        elif token.type == NOTEQ:
            self.eat(NOTEQ)
            print("IS NOTEQ")
        elif token.type == GT:
            self.eat(GT)
            print("IS GT")
        elif token.type == LESS:
            self.eat(LESS)
            print("IS LESS")
        elif token.type == GTEQ:
            self.eat(GTEQ)
            print("IS GTEQ")
        elif token.type == LESSEQ:
            self.eat(LESSEQ)
            print("IS LESSEQ")

        operator = token
        print("OPERATOR = ", operator)

        right_exp = self.Exp()

        self.eat(THEN)

        token = self.current_token

        destination_line = None
        if token.type == INTEGER:
            destination_line = token.value
            self.eat(INTEGER)
        
        return IfStatement(left_exp, operator, right_exp, destination_line)

    def For(self, line_number):
        """
            For : (FOR VAR EQUAL Exp TO Exp | FOR ID EQUAL Exp TO Exp STEP Exp) BStatement* INT NEXT VAR
        """
        self.enter_scope(line_number)

        print("(FOR)")
        self.eat(FOR)

        print("(VAR)")
        for_var = self.Var()

        print("(EQUAL)")
        for_assign_token = self.current_token
        self.eat(EQUAL)

        print("(EXP)")
        assign_exp = self.Exp()

        inside_assign = Assign(for_var, for_assign_token, assign_exp)

        print("(TO)")
        self.eat(TO)

        print("(EXP)")
        end_exp = self.Exp()

        step_exp = None

        if self.current_token.type == "STEP":
            print("(STEP)")
            self.eat(STEP)

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
        self.eat(NEXT)
        for_var = self.Var()

        current_scope_line = self.current_scope()
        self.exit_scope()
        return NextStatement(line_number, current_scope_line, for_var)

    def Remark(self):
        self.eat(REM)
        self.eat(ID) # sequencia de caracteres
        return self.empty()

    def parse(self):
        """
            Program : BStatement BStatement*

            BStatement : INTEGER Assign

            Assign : LET Var = Exp

            Var : ID

            Exp: Term (PLUS|MINUS Term)*

            Term: Eb ((MUL | DIV) Eb)*

            Eb: PLUS Eb | MINUS Eb | INTEGER | LPAREN Exp RPAREN | INTEGER | Var

            Print : PRINT Pitem (COMMA Pitem)* | (COMMA Pitem)* COMMA

            Pitem : Exp

            Goto : (GOTO | GO TO) Integer
            
            If : IF Exp (EQ | NOTEQ | GT | LESS | GTEQ | LESSEQ) Exp THEN INTEGER
            
            For : (FOR VAR EQUAL Exp TO Exp | FOR VAR EQUAL Exp TO Exp STEP Exp) BStatement* NEXT VAR

            Remark : REM (CHARACTER)*
        """
        print("*****************PARSE***********************")
        node = self.Program()
        if self.current_token.type != EOF:
            self.error()
        print("*****************END PARSE***********************")
        return node