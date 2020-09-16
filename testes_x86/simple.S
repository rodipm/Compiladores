	.data 								# Variaveis

										# Var1
	.globl	_var1
	.align 4
_var1:
	.long	5

										# Var2
	.globl	_var2
	.align 4
_var2:
	.long	6

										# Var3
	.comm	_var3, 4, 4



	.text								# Código


	.globl	_main
_main:
	movl	_var1, %eax
	addl	_var2, %eax
	subl	$3, %eax
	imul	$2, %eax
	movl	%eax, _var3
	ret

