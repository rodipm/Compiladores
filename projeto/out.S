	.data

.comm	_a, 4, 4


.text

	.globl	_main
_main:
	
	movl	$0, %eax
	movl	$2, %ecx
	movl	$2, %edx
	imul	%ecx, %edx
	movl	%edx, %eax
	
	addl	$1, %eax
	movl	$2, %ecx
	movl	$3, %edx
	imul	%ecx, %edx
	movl	%edx, %eax
	
	
	movl	%eax, _a
	
	ret
