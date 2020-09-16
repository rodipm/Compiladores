	.data

.comm	_a, 4, 4
.comm	_b, 4, 4
.comm	_c, 4, 4


.text

	.globl	_main
_main:
	
	movl	$0, %eax
	movl	$2, %edx
	addl	%edx, %eax
	addl	$3, %eax
	
	movl	%eax, %ecx
	movl	$5, %edx
	imul	%ecx, %edx
	movl	%edx, %eax
	
	movl	%eax, %ebx
	movl	$2, %ecx
	movl	$2, %edx
	imul	%ecx, %edx
	movl	%edx, %eax
	
	movl	$1, %edx
	addl	%edx, %eax
	
	addl	%ebx, %eax
	
	movl	$5, %ecx
	movl	$0, %edx
	idiv	%ecx
	movl	%eax, _a
	
	movl	$0, %eax
	movl	$10, %edx
	addl	%edx, %eax
	addl	_a, %eax
	
	movl	$8, %ecx
	movl	$0, %edx
	idiv	%ecx
	movl	%eax, _b
	
	movl	$0, %eax
	movl	_a, %edx
	addl	%edx, %eax
	addl	_b, %eax
	movl	%eax, _c
	
	ret
