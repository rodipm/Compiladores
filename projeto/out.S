	.section	.rdata,"dr"
LC0:
.ascii	"%d\12\0"

LC1:
.ascii	"%d\0"

LC2:
.ascii	"%d \0"
_string_0:
.ascii	"RESULTADO:\0"
_string_1:
.ascii	"FIM\0"
	.data

.comm	_N, 4, 4
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
.comm	_X, 36, 4


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



.text

.globl	_put
_put:
pushl	%ebp
movl	%esp, %ebp
subl	$24, %esp
movl	8(%ebp), %eax
movl	%eax, 4(%esp)
movl	$LC2, (%esp)
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
	movl	$2 ,%edx
	movl	%edx, _X+0
	
	label_21:
	movl	$0, %eax
	movl	$1 ,%edx
	movl	%edx, _X+4
	
	label_22:
	movl	$0, %eax
	movl	$4 ,%edx
	movl	%edx, _X+8
	
	label_23:
	movl	$0, %eax
	movl	$3 ,%edx
	movl	%edx, _X+12
	
	label_24:
	movl	$0, %eax
	movl	$5 ,%edx
	movl	%edx, _X+16
	
	label_25:
	movl	$0, %eax
	movl	$7 ,%edx
	movl	%edx, _X+20
	
	label_26:
	movl	$0, %eax
	movl	$6 ,%edx
	movl	%edx, _X+24
	
	label_90:
	movl	$0, %eax
	movl	$7 ,%edx
	movl	%edx, _N
	
	label_100:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _I_100
	movl	_N, %eax
	movl	$1,%edx
	subl	%edx, %eax
	
	movl	%eax ,_for_100_end_exp
	
	jmp for_100_control
	
	for_100_body:
	
	label_200:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _J_200
	movl	_N, %eax
	movl	$2,%edx
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
	movl	_J_200, %ebx
	 movl  _X(,%ebx, 4), %ecx
	movl	_NIDEX_200, %ebx
	 movl  _X(,%ebx, 4), %edx
	cmpl  %edx, %ecx
	jle    label_600
	
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
	pushl	$_string_0
	call	_print_string
	popl	%eax
	movl	$0, %eax
	label_900:
	movl	$0, %eax
	movl	$0 ,%edx
	movl	%edx, _A_900
	movl	_N, %eax
	movl	$1,%edx
	subl	%edx, %eax
	
	movl	%eax ,_for_900_end_exp
	
	jmp for_900_control
	
	for_900_body:
	
	label_910:
	movl	$0, %eax
	movl	_A_900, %ebx
	movl	_X(,%ebx, 4), %ebx
	pushl	%edx
	
	call _print
	popl %edx
	
	label_1000:
	
	movl	_A_900, %eax
	addl	$1, %eax
	movl	%eax, _A_900
	
	
	for_900_control:
	movl   _A_900, %eax
	movl  _for_900_end_exp, %ebx
	cmpl	%ebx, %eax
	jle	for_900_body
	
	label_1100:
	movl	$0, %eax
	pushl	$_string_1
	call	_print_string
	popl	%eax
	movl	$0, %eax
	leave
ret
