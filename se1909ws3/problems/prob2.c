#include <stdio.h>

int main()
{
    char n[101], d[] = {'6', '8', '4'};
    int i, s = 0;

    scanf("%s", n);
    
    for(i = n[0] == '-' ? 1 : 0; n[i]; i++)
        s += (n[i] - '0');

    printf("%c", d[s%3]);

    return 0;
}

