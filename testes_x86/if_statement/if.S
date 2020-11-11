	.section	.rodata
LC0:
	.string	"%d\n"
	.data

.text

.globl	_print
_print:
pushq	%rbp
movl	%esp, %ebp
subl	$24, %esp
movl	8(%ebp), %eax
movl	%eax, 4(%esp)
movl	$LC0, (%esp)
call	_printf
nop
leave
ret

	.globl	main
main:
	movl	$0, %eax
	
	movl	$5, %eax
	movl	$1,%edx
	addl	%edx, %eax
	
	movl	%eax, %edx
	movl	%edx, (%esp)
	call	_print
	movl	$0, %eax
	leave
ret
