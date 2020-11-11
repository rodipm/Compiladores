	.section	.rdata,"dr"
LC0:
.ascii	"%d\12\0"
	.data

.comm	_a, 4, 4
.comm	_b, 4, 4
.comm	_c, 4, 4


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
	
	label_10:
	movl	$0, %eax
	movl	$-7 ,%edx
	movl	%edx, _a
	
	label_20:
	movl	$0, %eax
	movl	$10 ,%edx
	movl	%edx, _b
	
	label_30:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _c
	
	label_40:
	movl	$0, %eax
	jmp label_50
	
	label_50:
	movl	$0, %eax
	movl	_a, %edx
	movl	%edx, (%esp)
	call	_print
	movl	$0, %eax
	label_60:
	movl	$0, %eax
	movl	_b, %edx
	movl	%edx, (%esp)
	call	_print
	movl	$0, %eax
	label_70:
	movl	$0, %eax
	movl	_c, %edx
	movl	%edx, (%esp)
	call	_print
	movl	$0, %eax
	leave
ret
