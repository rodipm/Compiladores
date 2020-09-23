	.data

.comm	_a, 4, 4
.comm	_b, 4, 4
.comm	_c, 4, 4
.comm	_d, 4, 4
.comm	_e, 4, 4
.comm	_f, 4, 4
.comm	_g, 4, 4
.comm	_h, 4, 4
.comm	_i, 4, 4


.text

	.globl	_main
_main:
	
	movl	$0, %eax
	movl	$4 ,%edx
	movl	%edx, _a
	
	movl	$0, %eax
	movl	$5 ,%edx
	movl	%edx, _b
	
	movl	$0, %eax
	movl	$1 ,%edx
	movl	%edx, _c
	
	movl	$0, %eax
	movl	$3 ,%edx
	movl	%edx, _d
	
	movl	$0, %eax
	movl	$2 ,%edx
	movl	%edx, _e
	
	movl	$0, %eax
	movl	_b, %eax
	movl	$3,%edx
	subl	%edx, %eax
	
	movl	%eax, %ecx
	movl	_b, %eax
	movl	$2,%edx
	addl	%edx, %eax
	
	movl	%eax, %edx
	imul	%ecx, %edx
	movl	%edx, %eax
	
	movl	%eax, %ebx
	movl	_a, %eax
	movl	$2, %ecx
	movl	$0, %edx
	idiv	%ecx
	
	addl	%ebx, %eax
	movl	%eax, _f
	
	movl	$0, %eax
	movl	_b, %ecx
	movl	$2, %eax
	movl	_c,%edx
	subl	%edx, %eax
	
	movl	%eax, %edx
	imul	%ecx, %edx
	movl	%edx, %eax
	movl	%eax, _g
	
	movl	$0, %eax
	movl	$1, %eax
	movl	$1,%edx
	addl	%edx, %eax
	
	addl	$1, %eax
	
	movl	_b, %edx
	addl	%edx, %eax
	movl	%eax, _h
	
	movl	$0, %eax
	movl	_f, %eax
	movl	_g,%edx
	addl	%edx, %eax
	
	addl	_h, %eax
	movl	%eax, _i
	
	ret
