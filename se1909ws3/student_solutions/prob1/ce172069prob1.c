#include <stdio.h>
#include <ctype.h>

int main() {
    char n[101];
    int count = 0;
    scanf("%s", n);
    for (int i = 0; n[i] != '\0'; i++) {
        if (isdigit(n[i])) {
            count++;
        }
    }
    printf("%d\n", count);
    return 0;
}
