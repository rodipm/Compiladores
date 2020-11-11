#include <stdio.h>

int x;
int y;
int main()
{
    x = 13;

    if (x >= 13)
    {
        y = 5;
    }
    else
    {
        y = 3;
    }
    printf("%d\n", y);
    return y;
}