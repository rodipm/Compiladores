	.section	.rdata,"dr"
LC0:
.ascii	"%d\12\0"
	.data

.comm	_a, 4, 4


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
	
	movl	$0, %eax
	movl	$-7 ,%edx
	movl	%edx, _a
	
	leave
ret
