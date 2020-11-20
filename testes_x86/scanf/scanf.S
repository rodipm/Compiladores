	.file	"scanf.c"
	.comm	_x, 20, 2
	.globl	_y
	.data
	.align 4
_y:
	.long	3
	.text
	.globl	__predef_rnd
	.def	__predef_rnd;	.scl	2;	.type	32;	.endef
__predef_rnd:
	pushl	%ebp
	movl	%esp, %ebp
	subl	$24, %esp
	movl	$0, (%esp)
	call	_time
	movl	%eax, (%esp)
	call	_srand
	call	_rand
	cltd
	idivl	8(%ebp)
	movl	%edx, %eax
	leave
	ret
LFE15:
	.def	___main;	.scl	2;	.type	32;	.endef
	.globl	_main
	.def	_main;	.scl	2;	.type	32;	.endef
_main:
LFB16:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	andl	$-16, %esp
	subl	$32, %esp
	call	___main
	movl	_y, %eax
	movl	%eax, (%esp)
	call	__predef_rnd
	movl	%eax, 28(%esp)
	movl	$1, %eax
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE16:
	.ident	"GCC: (MinGW.org GCC-6.3.0-1) 6.3.0"
	.def	_time;	.scl	2;	.type	32;	.endef
	.def	_srand;	.scl	2;	.type	32;	.endef
	.def	_rand;	.scl	2;	.type	32;	.endef
