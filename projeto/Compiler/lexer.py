from .token import *

class Lexer(object):

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self, ch):
        raise Exception('Caractere inválido: ' + ch)

    def advance(self):
        """
            Avanca para o proximo caractere a ser lido e atualiza o ponteiro de posicao atual
        """
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        """ 
            Obtem o proximo caractere sem avancar o ponteiro de posicao atual
        """ 
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return
        return self.text[peek_pos]

    def skip_whitespace(self):
        """
            Pula todos os caracteres vazios ate o proximo caractere valido
        """
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """
            Retorna um numeiro inteiro de multiplos digitos
        """
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return int(result)

    def _id(self):
        """
            Lida com identificadores e palavras reservadas
        """
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
            reserved = RESERVED_KEYWORDS.get(result)
            if reserved:
                print("RESERVED", reserved.type)
                if reserved.type == GO and not self.peek().isspace():
                    continue
                return reserved

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def _string(self):
        """
            Lida com reconhecimento de strings
        """
        self.advance() # first quote
        result = ''
        while self.current_char != "\"":
            result += self.current_char
            self.advance()
        
        self.advance() # second quote

        return Token(STRING, result)

    def get_next_token(self):
        """
            Obtem o proximo token do input
        """

        while self.current_char is not None:
            # Ignora caracteres em branco
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            else:
                if self.current_char.isalpha():
                    return self._id()
                if self.current_char.isdigit():
                    return Token(INTEGER, self.integer())
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            if self.current_char == '=':
                _t = None
                if self.peek() == '=':
                    _t = Token(EQ, '==')
                    self.advance()
                    self.advance()
                else:
                    _t = Token(EQUAL, '=')
                    self.advance()
                return _t
            if self.current_char == '>':
                _t = None
                if self.peek() == '=':
                    _t = Token(GTEQ, '>=')
                    self.advance()
                    self.advance()
                else:
                    _t = Token(GT, '>')
                    self.advance()
                return _t
            if self.current_char == '<':
                _t = None
                if self.peek() == '=':
                    _t = Token(LESSEQ, '<=')
                    self.advance()
                    self.advance()
                elif self.peek() == '>':
                    _t = Token(NOTEQ, '<>')
                    self.advance()
                    self.advance()
                else:
                    _t = Token(LESS, '<')
                    self.advance()
                return _t
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')
            if self.current_char == '[':
                self.advance()
                return Token(OPENBRACKET, '[')
            if self.current_char == ']':
                self.advance()
                return Token(CLOSEBRACKET, ']')
            if self.current_char == "\"":
                return self._string()
            self.error(self.current_char)


        return Token(EOF, None)