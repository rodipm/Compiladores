	.section	.rdata,"dr"
LC0:
.ascii	"%d\12\0"

LC1:
.ascii	"%d\0"
_string_0:
.ascii	"OK\0"
	.data

.comm	_for_100_end_exp, 4, 4
.comm	_for_200_end_exp, 4, 4
.comm	_for_600_end_exp, 4, 4
.comm	_for_700_end_exp, 4, 4
.comm	_I_100, 4, 4
.comm	_J_200, 4, 4
.comm	_A_600, 4, 4
.comm	_B_700, 4, 4
.comm	_X, 16, 2


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



	.globl	_main
_main:
pushl	%ebp
movl	%esp, %ebp
andl	$-16, %esp
subl	$16, %esp
call	___main
	
	label_1:
	movl	$0, %eax
	
	label_100:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _I_100
	movl	$1 ,_for_100_end_exp
	
	jmp for_100_control
	
	for_100_body:
	
	label_200:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _J_200
	movl	$1 ,_for_200_end_exp
	
	jmp for_200_control
	
	for_200_body:
	
	label_300:
	movl	$0, %eax
	
	movl	$0, %eax
	movl	$0, %ebx
	movl    _I_100, %edx
	
	addl	%edx, %eax
	movl    $2, %ecx
	imul    %ecx, %edx
	movl    %edx, %eax
	movl    _J_200, %edx
	
	addl	%edx, %eax
	movl	$0, %ebx
	addl	%eax, %ebx
	sall	$2, %ebx
	addl	$_X, %ebx
	movl  %ebx, (%esp)
	call _read
	
	label_400:
	
	movl	_J_200, %eax
	addl	$1, %eax
	movl	%eax, _J_200
	
	
	for_200_control:
	movl   _J_200, %eax
	movl  _for_200_end_exp, %ebx
	cmpl	%ebx, %eax
	jle	for_200_body
	
	label_500:
	
	movl	_I_100, %eax
	addl	$1, %eax
	movl	%eax, _I_100
	
	
	for_100_control:
	movl   _I_100, %eax
	movl  _for_100_end_exp, %ebx
	cmpl	%ebx, %eax
	jle	for_100_body
	
	label_550:
	movl	$0, %eax
	movl	$_string_0,(%esp)
	call	_print_string
	movl	$0, %eax
	label_600:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _A_600
	movl	$1 ,_for_600_end_exp
	
	jmp for_600_control
	
	for_600_body:
	
	label_700:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _B_700
	movl	$1 ,_for_700_end_exp
	
	jmp for_700_control
	
	for_700_body:
	
	label_800:
	movl	$0, %eax
	
	movl	$0, %eax
	movl	$0, %ebx
	movl    _A_600, %edx
	
	addl	%edx, %eax
	movl    $2, %ecx
	imul    %ecx, %edx
	movl    %edx, %eax
	movl    _B_700, %edx
	
	addl	%edx, %eax
	movl	$0, %ebx
	addl	%eax, %ebx
	movl	_X(,%ebx,4), %ebx
	movl  %ebx, (%esp)
	call _print
	
	label_900:
	
	movl	_B_700, %eax
	addl	$1, %eax
	movl	%eax, _B_700
	
	
	for_700_control:
	movl   _B_700, %eax
	movl  _for_700_end_exp, %ebx
	cmpl	%ebx, %eax
	jle	for_700_body
	
	label_1000:
	
	movl	_A_600, %eax
	addl	$1, %eax
	movl	%eax, _A_600
	
	
	for_600_control:
	movl   _A_600, %eax
	movl  _for_600_end_exp, %ebx
	cmpl	%ebx, %eax
	jle	for_600_body
	
	leave
ret
