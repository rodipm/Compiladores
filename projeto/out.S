	.section	.rdata,"dr"
LC0:
.ascii	"%d\12\0"
	.data

.comm	_X, 4, 4
.comm	_I_100, 4, 4


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
	
	label_100:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _I_100
	jmp for_100_control
	
	for_100_body:
	
	label_200:
	movl	$0, %eax
	movl	_I_100, %edx
	movl	%edx, (%esp)
	call	_print
	movl	$0, %eax
	
	movl	_I_100, %eax
	addl	$5, %eax
	movl	%eax, _I_100
	
	
	for_100_control:
	movl   _I_100, %eax
	cmpl	$20, %eax
	jle	for_100_body
	
	label_1000:
	movl	$0, %eax
	movl	_X, %edx
	movl	%edx, (%esp)
	call	_print
	movl	$0, %eax
	leave
ret
