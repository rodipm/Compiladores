# PCS PCS3566 - Linguagens e Compiladores

## Rodrigo Perrucci Macharelli - 9348877

# Projeto: Implementação de um compilador simples de Basic

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

If : IF Exp (GRTEQL | GRT | NOTEQL | LESSEQL | LESS | EQUAL) Exp THEN INTEGER

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

+ INTEGER
+ PLUS +
+ MINUS -
+ MUL *
+ DIV /
+ EQUAL =
+ GRTEQL >=
+ GRT >
+ NOTEQL <>
+ LESSEQL <=
+ LESS <
+ LPAREN (
+ RPAREN )
+ COMMA ,
+ QUOTES "
+ LET 
+ FN
+ READ
+ DATA
+ PRINT
+ GOTO
+ GO
+ TO
+ IF
+ THEN
+ FOR
+ TO
+ STEP
+ NEXT
+ DIM
+ DEF
+ GOSUB
+ RETURN
+ REM


## Versao simplificada para operacoes matematicas

```
Program : BStatement BStatement*

BStatement : INTEGER Assign

Assign : LET Var = Exp

Var : ID

Exp: Term (PLUS|MINUS Term)*

Term: Eb ((MUL | DIV) Eb)*

Eb: PLUS Eb | MINUS Eb | INTEGER | LPAREN Exp RPAREN | INTEGER | Var

ID: letter(digit|letter)*
```