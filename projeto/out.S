	.section	.rdata,"dr"
LC0:
.ascii	"%d\12\0"

LC1:
.ascii	"%d\0"
	.data

.comm	_X, 4, 4


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
	
	label_100:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _X
	
	label_200:
	movl	$0, %eax
	movl  $_X, (%esp)
	call _scan
	
	label_300:
	movl	$0, %eax
	movl	_X, %edx
	movl	%edx, (%esp)
	call	_print
	movl	$0, %eax
	leave
ret
