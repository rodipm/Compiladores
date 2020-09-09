import sys

from Compiler.lexer import Lexer
from Compiler.parser import Parser
from Compiler.code_generator import CodeGenerator

def main():
    # Obtendo o código fonte
    text = ""
    with open("source_code.basic") as f:
        text = f.read()

    # Efetuando as etapas de compilação
    lexer = Lexer(text)
    parser = Parser(lexer)
    code_gen = CodeGenerator(parser)
    result = code_gen.generate()

    # Mostra o resultado em linguagem de baixo nível
    print(result)
    with open('out.asm', 'w+') as (f):
        f.write(result)

if __name__ == '__main__':
    main()