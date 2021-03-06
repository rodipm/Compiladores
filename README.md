# PCS PCS3566 - Linguagens e Compiladores

## Rodrigo Perrucci Macharelli - 9348877

# Projeto: Implementação de um compilador simples do Dartmouth Basic

## Definindo a gramática

![Gramática Adotada](gramatica.png)

```
Program : BStatement BStatement* INTEGER END

BStatement : INTEGER Assign|Read|Data|Print|Goto|If|For|Next|Dim|Def|Gosub|Return|Remark

Assign : LET Var EQUAL Exp

Var : ID
    | ID LPAREN Exp (COMMA Exp)* RPAREN

Exp: Term (PLUS|MINUS Term)*

Term: Eb ((MUL | DIV) Eb)*

Eb: LPAREN Exp RPAREN| INTEGER |Var|FN letter LPAREN Exp RPAREN

Read : READ Var (COMMA Var)*

Data : DATA Snum (COMMA Snum)*

Print : PRINT  
      | PRINT Pitem (COMMA Pitem)* | (COMMA Pitem)* COMMA

Pitem : Exp | QUOTES CHARACTER(CHARACTER)* QUOTES (Exp)*

Goto : (GOTO | GO TO) Integer

If : IF Exp (EQ | NOTEQ | GT | LESS | GTEQ | LESSEQ) Exp THEN INTEGER

For : FOR ID EQUAL Exp TO Exp | FOR ID EQUAL Exp TO Exp STEP Exp

Next : NEXT ID

Dim : DIM ID LPAREN INTEGER (COMMA INTEGER)* RPAREN (COMMA ID LPAREN INTEGER (COMMA INTEGER)* RPAREN) *

Def : DEF FN ID LPAREN ID RPAREN EQUAL Exp

Gosub : GOSUB INTEGER

Return : RETURN

Remark : REM (CHARACTER)*

Snum = PLUS | MINUS INTEGER

INTEGER: digit(digit)*

CHARACTER = letter | digit | special

ID: letter(digit|letter)*
```

## Terminais

\item INTEGER
\item PLUS \item
\item MINUS -
\item MUL *
\item DIV /
\item EQUAL =
\item EQ ==
\item GTEQ >=
\item GT >
\item NOTEQ <>
\item LESSEQ <=
\item LESS <
\item LPAREN (
\item RPAREN )
\item COMMA ,
\item QUOTES "
\item LET 
\item FN
\item READ
\item DATA
\item PRINT
\item GOTO
\item GO
\item TO
\item IF
\item THEN
\item FOR
\item TO
\item STEP
\item NEXT
\item DIM
\item DEF
\item GOSUB
\item RETURN
\item REM


## Versao simplificada para operacoes aritméticas

```
Program : BStatement BStatement*

BStatement : INTEGER Assign | Remark

Assign : LET Var = Exp

Var : ID

Exp: Term (PLUS|MINUS Term)*

Term: Eb ((MUL | DIV) Eb)*

Eb: PLUS Eb | MINUS Eb | INTEGER | LPAREN Exp RPAREN | INTEGER | Var | FN letter LPAREN Exp RPAREN

Remark : REM (CHARACTER)*

ID: letter(digit|letter)*
```

Após feitos testes, pode-se verificar a funcionalidade da geração de código e interpretação do código fonte, sendo capaz de declarar variáveis e utiliza-las em expressões aritméticas (adição, subtração, multiplicação e divisão) utilizando instruções de máquina geradas em x86 assembly, sendo o código assembly montado com auxílio do gcc.


## Incluindo novas regras de formação


```
Program : BStatement BStatement*

BStatement : INTEGER Assign | PRINT | GOTO | IF | FOR | NEXT | DEF | Remark

Assign : LET Var = Exp

Var : ID | ID[Exp (, Exp)*]

Exp: Term (PLUS|MINUS Term)*

Term: Eb ((MUL | DIV) Eb)*

Eb: PLUS Eb | MINUS Eb | INTEGER | LPAREN Exp RPAREN | INTEGER | Var

Read : READ Var

Print : PRINT  
      | PRINT Pitem (COMMA Pitem)* | (COMMA Pitem)* COMMA

Pitem : Exp

Goto : (GOTO | GO TO) Integer

If : IF Exp (EQ | NOTEQ | GT | LESS | GTEQ | LESSEQ) Exp THEN INTEGER

For : FOR ID EQUAL Exp TO Exp | FOR ID EQUAL Exp TO Exp STEP Exp

Next : NEXT ID

Def : DEF FN ID LPAREN ID RPAREN EQUAL Exp

Dim : DIM ID LPAREN INTEGER (COMMA INTEGER)* RPAREN (COMMA ID LPAREN INTEGER (COMMA INTEGER)* RPAREN) *

Remark : REM (CHARACTER)*

ID: letter(digit|letter)*
```


DIM VAR(a) = [0, ..., a-1] -> VAR(n) = VAR(n)

DIM(a, b) = 
[
      [0, ..., b-1],
      [b, ..., 2b-1]
]
 -> VAR(n, m) = n*b
