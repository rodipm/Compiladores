	.file	"teste.c"
	.def	___main;	.scl	2;	.type	32;	.endef
	.text
	.globl	_main
_main:
	movl	$2, 12(%esp) 	# a = 2
	movl	$3, 8(%esp) 	# b = 3 
	movl	$1, 4(%esp)		# c = 1
	movl	12(%esp), %eax
	imull	8(%esp), %eax # a * b
	movl	%eax, %edx
	movl	4(%esp), %eax
	addl	%eax, %edx
	movl	12(%esp), %eax
	imull	12(%esp), %eax
	addl	%edx, %eax
	ret

