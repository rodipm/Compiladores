#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int x[5];
int y = 3;

int _predef_rnd(char *x) {
    puts(x);
    puts("poals");
    return 5;
}

int main()
{
    // x[0] = 1;
    // x[y] = 2;
    // x[2] = 3;
    int x = _predef_rnd("oi");
    return 1;
}