#include <stdio.h>

int main() {
    int a, b;
    scanf("%d %d", &a, &b);
    if (a > b) {
        int temp = a;
        a = b;
        b = temp;
    }
    for (int i = a; i <= b; i++) {
        for (int j = 1; j <= 9; j++) {
            printf("%d x %d = %d\n", i, j, i * j);
        }
    }
    return 0;
}
