	.file	"scanf.c"
	.comm	_x, 20, 2
	.globl	_y
	.data
	.align 4
_y:
	.long	3
	.section .rdata,"dr"
LC0:
	.ascii "%d\12\0"
	.text
	.globl	_scan
	.def	_scan;	.scl	2;	.type	32;	.endef
_scan:
LFB10:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$24, %esp
	movl	8(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC0, (%esp)
	call	_scanf
	nop
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE10:
	.def	___main;	.scl	2;	.type	32;	.endef
	.globl	_main
	.def	_main;	.scl	2;	.type	32;	.endef
_main:
LFB11:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	andl	$-16, %esp
	subl	$16, %esp
	call	___main
	movl	$1, _x
	movl	_y, %eax
	movl	$2, _x(,%eax,4)
	movl	$3, _x+8
	movl	_y, %eax
	sall	$2, %eax
	addl	$_x, %eax
	movl	%eax, (%esp)
	call	_scan
	movl	_x+4, %eax
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE11:
	.ident	"GCC: (MinGW.org GCC-6.3.0-1) 6.3.0"
	.def	_scanf;	.scl	2;	.type	32;	.endef
