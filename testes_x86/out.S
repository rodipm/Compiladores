	.data

.comm	_a, 4, 4


.text

	.globl	_main
_main:
	movl	$6, %eax
	addl	$5, %eax
	movl	%eax, _a
	
	ret
