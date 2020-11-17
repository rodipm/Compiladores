	.section	.rdata,"dr"
LC0:
.ascii	"%d\12\0"

LC1:
.ascii	"%d\0"
	.data

.comm	_X, 4, 4
.comm	_S, 4, 4
.comm	_for_200_end_exp, 4, 4
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
addl	$24, %esp
movl	%ebp, %esp
nop
leave
ret

.globl	_scan
_scan:
pushl	%ebp
movl	%esp, %ebp
subl	$24, %esp
movl	8(%ebp), %eax
movl	%eax, 4(%esp)
movl	$LC1, (%esp)
call	_scanf
addl	$24, %esp
movl	%ebp, %esp
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
	
	label_60:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _S
	
	label_200:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _J_200
	movl	$3 ,_for_200_end_exp
	
	jmp for_200_control
	
	for_200_body:
	
	label_250:
	movl	$0, %eax
	movl  $_X, (%esp)
	call _scan
	
	label_300:
	movl	$0, %eax
	movl	_S, %eax
	movl	_X,%edx
	addl	%edx, %eax
	movl	%eax, _S
	
	
	movl	_J_200, %eax
	addl	$1, %eax
	movl	%eax, _J_200
	
	
	for_200_control:
	movl   _J_200, %eax
	movl  _for_200_end_exp, %ebx
	cmpl	%ebx, %eax
	jle	for_200_body
	
	label_500:
	movl	$0, %eax
	movl	_S, %edx
	movl	%edx, (%esp)
	call	_print
	movl	$0, %eax
	leave
ret
