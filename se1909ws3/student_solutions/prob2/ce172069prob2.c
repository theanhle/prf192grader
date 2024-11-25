#include <stdio.h>

int main() {
    long long n;
    scanf("%lld", &n);
    int best_digit = -1;
    for (int i = 0; i <= 9; i++) {
        long long new_number = n * 10 + i;
        if (new_number % 6 == 0) {
            best_digit = i;
        }
    }
    printf("%d\n", best_digit);
    return 0;
}
