	.section	.rdata,"dr"
LC0:
.ascii	"%d\12\0"

LC1:
.ascii	"%d\0"
	.data

.comm	_Y, 4, 4
.comm	_X, 8, 2


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
	
	label_5:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _Y
	
	label_10:
	movl	$0, %eax
	
	label_20:
	movl	$0, %eax
	movl	$5 ,%edx
	movl   _Y, %ebx
	movl	%edx, _X(,%ebx,4)
	
	label_25:
	movl	$0, %eax
	movl	_Y, %eax
	movl	$1,%edx
	addl	%edx, %eax
	movl	%eax, _Y
	
	label_30:
	movl	$0, %eax
	movl	$10 ,%edx
	movl   _Y, %ebx
	movl	%edx, _X(,%ebx,4)
	
	label_50:
	movl	$0, %eax
	
	movl	_X+4, %eax
	movl	_X+0,%edx
	addl	%edx, %eax
	
	movl	%eax, %edx
	movl	%edx, (%esp)
	call	_print
	movl	$0, %eax
	leave
ret
