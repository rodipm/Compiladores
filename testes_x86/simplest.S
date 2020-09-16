	.text
	.globl	_main
_main:
	movl	$5, %eax
	addl	$6, %eax
	subl	$3, %eax
	imul    $2, %eax
	ret
