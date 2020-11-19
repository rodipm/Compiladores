#include <stdio.h>

int a[5][13];
int x = 3;
int y = 1;
int main()
{
    a[x][y] = 1;
    a[1][1] = a[x][y] + 1;

    printf("%d\n", a[x+y][y+5]);
    return 1;
}

// (x)*4 - 1d VAR[x]
// (y + DIM2*(x))*4 - 2d VAR[x, y] = [DIM1, DIM2]
// (z + DIM3*(y + DIM2*(x)))*4 - 3d VAR[x, y, z] = [DIM1, DIM2, DIM3]
// (w + DIM4*(z + DIM3*(y + DIM2*(x))))*4 - 4d VAR[x, y, z, w] = [DIM1, DIM2, DIM3, DIM4]

/*
    # x
	movl	_x, %edx

	# y
	movl	$13, %ecx 	# Dim2
	imul	%ecx, %edx
	movl	%edx, %eax

	movl	_y, %edx
	addl	%eax, %edx

	# z
	movl	$21, %ecx 	# Dim2
	imul	%ecx, %edx
	movl	%edx, %eax

	movl	_z, %edx
	addl	%eax, %edx

	#Ajuste para tamanho 4
	movl	%edx, %eax
	movl	$4, _a(,%eax,4)
*/