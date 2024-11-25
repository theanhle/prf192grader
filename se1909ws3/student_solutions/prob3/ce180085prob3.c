#include <stdio.h>


void print_multiplication_table(int num)
{
    for (int i = 1; i <= 9; i++)
    {
        printf("%d x %d = %d\n", num, i, num * i);
    }
}
int main()
{
    int a, b;
    scanf("%d %d", &a, &b);
    for (int i = a; i <= b; i++)
    {
        print_multiplication_table(i);
    }

    return 0;
}
