	.section	.rdata,"dr"
LC0:
.ascii	"%d\12\0"

LC1:
.ascii	"%d\0"
	.data

.comm	_for_100_end_exp, 4, 4
.comm	_SOMA, 4, 4
.comm	_X, 4, 4
.comm	_for_400_end_exp, 4, 4
.comm	_I_100, 4, 4
.comm	_J_400, 4, 4
.comm	_INPUTS, 12, 2


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
	
	label_10:
	movl	$0, %eax
	
	label_100:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _I_100
	movl	$2 ,_for_100_end_exp
	
	jmp for_100_control
	
	for_100_body:
	
	label_200:
	movl	$0, %eax
	movl	_I_100, %eax
	sall	$2, %eax
	addl	$_INPUTS, %eax
	movl  %eax, (%esp)
	call _scan
	
	label_300:
	
	movl	_I_100, %eax
	addl	$1, %eax
	movl	%eax, _I_100
	
	
	for_100_control:
	movl   _I_100, %eax
	movl  _for_100_end_exp, %ebx
	cmpl	%ebx, %eax
	jle	for_100_body
	
	label_350:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _SOMA
	
	label_360:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _X
	
	label_400:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _J_400
	movl	$1 ,_for_400_end_exp
	
	jmp for_400_control
	
	for_400_body:
	
	label_500:
	movl	$0, %eax
	movl	movl	_J_400, %eax
	movl	$1,%edx
	addl	%edx, %eax
	, %ebx
	movl	_INPUTS(,%ebx, 4), %ebx
	movl  %ebx, (%esp)
	call _print
	
	label_600:
	
	movl	_J_400, %eax
	addl	$1, %eax
	movl	%eax, _J_400
	
	
	for_400_control:
	movl   _J_400, %eax
	movl  _for_400_end_exp, %ebx
	cmpl	%ebx, %eax
	jle	for_400_body
	
	leave
ret
