	.section	.rdata,"dr"
LC0:
.ascii	"%d\12\0"

LC1:
.ascii	"%d\0"
_string_0:
.ascii	"RETURNED\0"
_string_1:
.ascii	"END\0"
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

.globl	_print_string
_print_string:
pushl	%ebp
movl	%esp, %ebp
subl	$24, %esp
movl	8(%ebp), %eax
movl	%eax, (%esp)
call	_puts
nop
leave
ret

.globl	_read
_read:
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

.globl	_predef_rnd
_predef_rnd:
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
addl	$24, %esp
movl	%ebp, %esp
leave
ret



	.globl	_main
_main:
pushl	%ebp
movl	%esp, %ebp
andl	$-16, %esp
subl	$16, %esp
call	___main
	
	label_1:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _X
	
	label_10:
	movl	$0, %eax
	call label_110
	
	label_20:
	movl	$0, %eax
	pushl	$_string_0
	call	_print_string
	popl	%eax
	movl	$0, %eax
	label_15:
	movl	$0, %eax
	movl	_X, %edx
	pushl	%edx
	call	_print
	
	popl	%eax
	movl	$0, %eax
	label_30:
	movl	$0, %eax
	jmp label_500
	
	label_110:
	movl	$0, %eax
	movl $20, %eax
	pushl	%eax
	call   _predef_rnd
	popl	%ebx
	movl	%eax, _X
	
	label_120:
	movl	$0, %eax
	ret
	
	label_500:
	movl	$0, %eax
	pushl	$_string_1
	call	_print_string
	popl	%eax
	movl	$0, %eax
	leave
ret
