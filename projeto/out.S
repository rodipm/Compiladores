	.section	.rdata,"dr"
LC0:
.ascii	"%d\12\0"
	.data

.comm	_X, 4, 4
.comm	_J_200, 4, 4


.text

.globl	_print
_print:
pushl	%ebp
movl	%esp, %ebp
subl	$24, %esp
movl	8(%ebp), %eax
movl	%eax, 4(%esp)
movl	$LC0, (%esp)
call	_printf
nop
leave
ret

	.globl	_main
_main:
pushl	%ebp
movl	%esp, %ebp
andl	$-16, %esp
subl	$16, %esp
call	___main
	
	label_50:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _X
	
	label_200:
	movl	$0, %eax
	movl	_X, %eax
	movl	$1,%edx
	addl	%edx, %eax
	movl	%eax, _J_200
	movl	_X, %eax
	movl	$5,%edx
	addl	%edx, %eax
	
	movl	%eax ,%ebx
	movl	%ebx, (%esp)
	
	jmp for_200_control
	
	for_200_body:
	
	label_300:
	movl	$0, %eax
	movl	_X, %eax
	movl	$1,%edx
	addl	%edx, %eax
	movl	%eax, _X
	
	
	movl	_J_200, %eax
	addl	$1, %eax
	movl	%eax, _J_200
	
	
	for_200_control:
	movl   _J_200, %eax
	movl  (%esp), %ebx
	cmpl	%ebx, %eax
	jle	for_200_body
	
	leave
ret
