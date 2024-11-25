#include <stdio.h>
int count_digits()
{
    char c;
    int digit_count = 0;
    while ((c = getchar()) != '\n')
    {
        if (c >= '0' && c <= '9')
        {
            digit_count++;
        }
    }
    return digit_count;
}

int main()
{
    int result = count_digits();
    printf("%d\n", result);
    return 0;
}
