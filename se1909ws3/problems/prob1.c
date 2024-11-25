#include <stdio.h>
#include <ctype.h>

int main()
{
    char s[102];
    int i, n = 0;

    scanf("%[^\n]", s);

    for(i = 0; s[i]; i++)
        n += isdigit(s[i]);

    printf("%d", n);

    return 0;
}

