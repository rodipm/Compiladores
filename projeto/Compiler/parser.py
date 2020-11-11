from .ast import *
from .token import *

class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

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
            BStatement : INTEGER Assign | PRINT | If | Remark
        """
        print("(BStatement)")
        node = None
        self.eat(INTEGER)
        print("->INTEGER->")
        if self.current_token.type == LET:
            node = self.Assign()
        elif self.current_token.type == REM:
            node = self.Remark()
        elif self.current_token.type == IF:
            node = self.If()
        elif self.current_token.type == PRINT:
            node = self.Print()
        return node

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
        node = Var(self.current_token)
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

    def If(self):
        """
            If : IF Exp (GRTEQL | GRT | NOTEQL | LESSEQL | LESS | EQUAL) Exp THEN INTEGER
        """
        print("(IF)")
        self.eat(IF)
        left_exp = self.Exp()

        token = self.current_token
        operator = None
        if token.type == EQ:
            self.eat(EQ)
            print("IS EQ")
        operator = token
        print("OPERATOR = ", operator)

        right_exp = self.Exp()

        self.eat(THEN)

        token = self.current_token
        line = None
        if token.type == INTEGER:
            line = token.value
            self.eat(INTEGER)
        
        return IfStatement(left_exp, operator, right_exp, line)

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

            If : IF Exp (GRTEQL | GRT | NOTEQL | LESSEQL | LESS | EQUAL) Exp THEN INTEGER

            Remark : REM (CHARACTER)*
        """
        print("*****************PARSE***********************")
        node = self.Program()
        if self.current_token.type != EOF:
            self.error()
        print("*****************END PARSE***********************")
        return node