	.section	.rdata,"dr"
LC0:
.ascii	"%d\12\0"

LC1:
.ascii	"%d\0"
_string_0:
.ascii	"OK\0"
_string_1:
.ascii	"THEN\0"
_string_2:
.ascii	"FIM\0"
	.data

.comm	_for_100_end_exp, 4, 4
.comm	_for_200_end_exp, 4, 4
.comm	_for_900_end_exp, 4, 4
.comm	_I_100, 4, 4
.comm	_J_200, 4, 4
.comm	_NIDEX_200, 4, 4
.comm	_CUR_200, 4, 4
.comm	_NVAL_200, 4, 4
.comm	_TEMP_200, 4, 4
.comm	_A_900, 4, 4
.comm	_X, 12, 2


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
	
	label_10:
	movl	$0, %eax
	
	label_20:
	movl	$0, %eax
	movl	$30 ,%edx
	movl	%edx, _X+0
	
	label_30:
	movl	$0, %eax
	movl	$20 ,%edx
	movl	%edx, _X+4
	
	label_40:
	movl	$0, %eax
	movl	$10 ,%edx
	movl	%edx, _X+8
	
	label_100:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _I_100
	movl	$3 ,_for_100_end_exp
	
	jmp for_100_control
	
	for_100_body:
	
	label_200:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _J_200
	movl	$2, %eax
	movl	$1,%edx
	subl	%edx, %eax
	
	subl	_I_100, %eax
	
	movl	%eax ,_for_200_end_exp
	
	jmp for_200_control
	
	for_200_body:
	
	label_210:
	movl	$0, %eax
	movl	_J_200, %eax
	movl	$1,%edx
	addl	%edx, %eax
	movl	%eax, _NIDEX_200
	
	label_211:
	movl	$0, %eax
	movl	_J_200, %ebx
	movl	_X(,%ebx, 4), %ebx
	movl  %ebx, (%esp)
	call _print
	
	movl	_NIDEX_200, %ebx
	movl	_X(,%ebx, 4), %ebx
	movl  %ebx, (%esp)
	call _print
	
	label_212:
	movl	$0, %eax
	
	movl    _J_200, %edx
	
	addl	%edx, %eax
	movl	$0, %ebx
	addl	%eax, %ebx
	movl	_X(,%ebx,4) ,%edx
	movl	%edx, _CUR_200
	
	label_213:
	movl	$0, %eax
	
	movl    _NIDEX_200, %edx
	
	addl	%edx, %eax
	movl	$0, %ebx
	addl	%eax, %ebx
	movl	_X(,%ebx,4) ,%edx
	movl	%edx, _NVAL_200
	
	label_215:
	movl	$0, %eax
	movl  _CUR_200, %ecx
	movl	_NVAL_200, %edx
	cmpl  %edx, %ecx
	jl    label_260
	
	label_216:
	movl	$0, %eax
	movl	$_string_0,(%esp)
	call	_print_string
	movl	$0, %eax
	label_220:
	movl	$0, %eax
	
	movl    _J_200, %edx
	
	addl	%edx, %eax
	movl	$0, %ebx
	addl	%eax, %ebx
	movl	_X(,%ebx,4) ,%edx
	movl	%edx, _TEMP_200
	
	label_230:
	movl	$0, %eax
	movl   _J_200, %ebx
	push	%ebx
	
	
	movl	$0, %eax
	movl    _NIDEX_200, %edx
	
	addl	%edx, %eax
	movl	$0, %ebx
	addl	%eax, %ebx
	movl	_X(,%ebx,4), %eax
	pop	%ebx
	movl	%eax, _X(,%ebx,4)
	
	label_240:
	movl	$0, %eax
	movl	_TEMP_200 ,%edx
	movl   _NIDEX_200, %ebx
	movl	%edx, _X(,%ebx,4)
	
	label_250:
	movl	$0, %eax
	movl	_J_200, %ebx
	movl	_X(,%ebx, 4), %ebx
	movl  %ebx, (%esp)
	call _print
	
	label_260:
	movl	$0, %eax
	movl	$_string_1,(%esp)
	call	_print_string
	movl	$0, %eax
	label_600:
	
	movl	_J_200, %eax
	addl	$1, %eax
	movl	%eax, _J_200
	
	
	for_200_control:
	movl   _J_200, %eax
	movl  _for_200_end_exp, %ebx
	cmpl	%ebx, %eax
	jle	for_200_body
	
	label_700:
	
	movl	_I_100, %eax
	addl	$1, %eax
	movl	%eax, _I_100
	
	
	for_100_control:
	movl   _I_100, %eax
	movl  _for_100_end_exp, %ebx
	cmpl	%ebx, %eax
	jle	for_100_body
	
	label_800:
	movl	$0, %eax
	movl	$_string_2,(%esp)
	call	_print_string
	movl	$0, %eax
	label_900:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _A_900
	movl	$2 ,_for_900_end_exp
	
	jmp for_900_control
	
	for_900_body:
	
	label_910:
	movl	$0, %eax
	movl	_A_900, %ebx
	movl	_X(,%ebx, 4), %ebx
	movl  %ebx, (%esp)
	call _print
	
	label_1000:
	
	movl	_A_900, %eax
	addl	$1, %eax
	movl	%eax, _A_900
	
	
	for_900_control:
	movl   _A_900, %eax
	movl  _for_900_end_exp, %ebx
	cmpl	%ebx, %eax
	jle	for_900_body
	
	leave
ret
