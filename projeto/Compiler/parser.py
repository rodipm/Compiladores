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

        nodes = [node]

        while self.current_token.type == INTEGER:
            nodes.append(self.BStatement())

        root = StatementList()
        for node in nodes:
            root.children.append(node)

        return root

    def BStatement(self):
        """
            BStatement : INTEGER Assign
        """
        self.eat(INTEGER)
        node = self.Assign()
        return node

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

    def Var(self):
        """
            Var : ID
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def Exp(self):
        """
            Exp: Term (PLUS|MINUS Term)*
        """
        node = self.Term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            else:
                if token.type == MINUS:
                    self.eat(MINUS)
            node = BinOp(left=node, op=token, right=(self.Term()))

        return node

    def Term(self):
        """
            Term: Eb ((MUL | DIV) Eb)*
        """
        node = self.Eb()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            else:
                if token.type == DIV:
                    self.eat(DIV)
            node = BinOp(left=node, op=token, right=(self.Eb()))

        return node

    def Eb(self):
        """
            Eb : PLUS Eb
                  | MINUS Eb
                  | INTEGER
                  | LPAREN Exp RPAREN
                  | Var
        """
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.Eb())
            return node
        if token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.Eb())
            return node
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        if token.type == LPAREN:
            self.eat(LPAREN)
            node = self.Exp()
            self.eat(RPAREN)
            return node
        node = self.Var()
        return node

    def parse(self):
        """
            Program : BStatement BStatement*

            BStatement : INTEGER Assign

            Assign : LET Var = Exp

            Var : ID

            Exp: Term (PLUS|MINUS Term)*

            Term: Eb ((MUL | DIV) Eb)*

            Eb: PLUS Eb | MINUS Eb | INTEGER | LPAREN Exp RPAREN | INTEGER | Var
        """
        node = self.Program()
        if self.current_token.type != EOF:
            self.error()
        return node