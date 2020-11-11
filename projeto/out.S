	.section	.rdata,"dr"
LC0:
.ascii	"%d\12\0"
	.data

.comm	_a, 4, 4
.comm	_b, 4, 4
.comm	_c, 4, 4
.comm	_d, 4, 4


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
	movl	$10 ,%edx
	movl	%edx, _a
	
	label_20:
	movl	$0, %eax
	movl	$10 ,%edx
	movl	%edx, _b
	
	label_30:
	movl	$0, %eax
	movl	$5 ,%edx
	movl	%edx, _c
	
	label_40:
	movl	$0, %eax
	movl	$15 ,%edx
	movl	%edx, _d
	
	label_100:
	movl	$0, %eax
	movl	_a, %eax
	movl	_b,%edx
	addl	%edx, %eax
	
	addl	_c, %eax
	
	movl	%eax, %ecx
	movl	$2, %edx
	imul	%ecx, %edx
	movl	%edx, %eax
	 movl %eax, %ecx
	movl	$25, %ecx
	movl	$2, %edx
	imul	%ecx, %edx
	movl	%edx, %eax
	movl %eax, %edx
	cmpl  %edx, %ecx
	jne    label_300
	
	label_200:
	movl	$0, %eax
	movl	$200, %edx
	movl	%edx, (%esp)
	call	_print
	movl	$0, %eax
	label_210:
	movl	$0, %eax
	jmp label_500
	
	label_300:
	movl	$0, %eax
	movl	$300, %edx
	movl	%edx, (%esp)
	call	_print
	movl	$0, %eax
	label_500:
	movl	$0, %eax
	movl	$12345, %edx
	movl	%edx, (%esp)
	call	_print
	movl	$0, %eax
	leave
ret
