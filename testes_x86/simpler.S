	.data

	.globl	_var1
	.align 4
_var1:
	.long	5

	.globl	_var2
	.align 4
_var2:
	.long	6

	.text

	.globl	_main
_main:
	movl	_var1, %eax
	addl	_var2, %eax
	subl	$3, %eax
	imul	$2, %eax
	ret
