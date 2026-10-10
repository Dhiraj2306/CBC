#include <string.h>
#define MAX 100

int isPalindrome(char str[]) 
{
    char stack[MAX];
    int top = -1;
    int i;

    // Push all characters onto stack
    for (i = 0; str[i] != '\0'; i++) 
    {
        stack[++top] = str[i];
    }
    // Compare characters by popping from stack
    for (i = 0; str[i] != '\0'; i++) 
    {
        if (str[i] != stack[top--]) 
        {
            return 0;   // Not a palindrome
        }
    }

    return 1;           // Palindrome
}


