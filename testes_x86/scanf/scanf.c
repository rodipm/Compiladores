#include <stdio.h>

int x[5];
int y = 3;

void scan(int *x) {
    scanf("%d\n", x);
}
int main()
{
    x[0] = 1;
    x[y] = 2;
    x[2] = 3;

    scan(&x[y]);
    return x[1];
}