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
        node = self.BStatement()

        results = [node]

        while self.current_token.type == INTEGER:
            results.append(self.BStatement())

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def BStatement(self):
        """
            BStatement : INTEGER Assign
        """
        self.eat(INTEGER)
        nodes = self.statement_list()


        return root

    def Assign(self):
        """
            Assign : LET Var EQUAL Exp
        """
        self.eat(LET)

        left = self.Var()

        token = self.current_token
        self.eat(EQUAL)

        right = self.Exp()

        node = Assign(left, token, right)
        return node


    def Exp(self):
        """
        expr : term ((PLUS | MINUS) term)*
        """
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            else:
                if token.type == MINUS:
                    self.eat(MINUS)
            node = BinOp(left=node, op=token, right=(self.term()))

        return node

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            else:
                if token.type == DIV:
                    self.eat(DIV)
            node = BinOp(left=node, op=token, right=(self.factor()))

        return node

    def factor(self):
        """factor : PLUS factor
                  | MINUS factor
                  | INTEGER
                  | LPAREN expr RPAREN
                  | variable
        """
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        if token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        if token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        node = self.variable()
        return node

    def parse(self):
        """
            Program : BStatement BStatement*

            BStatement : INTEGER Assign

            Assign : LET Var = Exp

            Var : (letter digit|letter) 
                | (letter digit|letter) LPAREN Exp (COMMA Exp)* RPAREN

            Exp: Term (PLUS|MINUS Term)*

            Term: Eb ((MUL | DIV) Eb)*

            Eb: PLUS Eb | MINUS Eb | INTEGER | LPAREN Exp RPAREN | INTEGER | Var
        """
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node