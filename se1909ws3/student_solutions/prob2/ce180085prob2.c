#include <stdio.h>
#include <string.h>

// Function to find the largest digit that can be appended to make the number divisible by 6
int find_largest_digit(char n[]) {
    int sum = 0;
    int last_digit = n[strlen(n) - 1] - '0'; // Get the last digit

    // Calculate the sum of the digits
    for (int i = 0; i < strlen(n); i++) {
        sum += n[i] - '0'; // Convert char to int and add to sum
    }

    // Check digits from 9 to 0
    for (int digit = 9; digit >= 0; digit--) {
        // Check if appending this digit makes the number even and the sum of digits divisible by 3
        if ((last_digit * 10 + digit) % 2 == 0 && (sum + digit) % 3 == 0) {
            return digit; // Return the first valid digit found
        }
    }

    return -1; // Return -1 if no valid digit is found
}

int main() {
    char n[102]; // Array to hold the input number as a string
    scanf("%s", n); // Read the input number

    int result = find_largest_digit(n); // Call the function to find the largest digit

    // Print the result
    if (result != -1) {
        printf("%d\n", result); // Print the largest valid digit
    } else {
        printf("No valid digit found\n"); // Print message if no valid digit was found
    }

    return 0; // Single return statement in the main function
}
