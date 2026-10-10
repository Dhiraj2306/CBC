//2.

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#define SIZE 20

struct stack
{
    int top;
    char data[SIZE];
};
typedef struct stack STACK;

void push(STACK *s, char item)
{
    s->data[++(s->top)] = item;
}

char pop(STACK *s)
{
    return s->data[(s->top)--];
}

char preced(char symbol)
{
    switch (symbol)
    {
        case '+':
        case '-': return 1;
        case '*':
        case '/': return 3;
        case '^': return 5;
        default: return 0;
    }
}

// infix to postfix function
// Pass postfix as an output parameter
int infix_to_postfix(STACK *s, char infix[20], char postfix[20])
{
    int i, j = 0;
    char symbol, temp;

    for (i = 0; infix[i] != '\0'; i++)
    {
        symbol = infix[i];
        if (isalnum(symbol))
            postfix[j++] = symbol;
        else
        {
            switch (symbol)
            {
                case '(':
                    push(s, symbol);
                    break;
                case ')':
                    temp = pop(s);
                    while (temp != '(') 
                    {
                        postfix[j++] = temp;
                        temp = pop(s);

                    }
                    break;
                case '+':
                case '-':
                case '^':
                case '*':
                case '/':
                    if (s->top == -1 || s->data[s->top] == '(')
                        push(s, symbol);
                    else
                    {
                        while (s->top != -1 && s->data[s->top] != '(' && preced(s->data[s->top]) >= preced(symbol))
                        {
                            postfix[j++] = pop(s);
                        }
                        push(s, symbol);
                    }
                    break;
                default:
                    printf("Invalid symbol in expression: %c\n", symbol);
                    return 0; // Indicate error
            }
        }
    }
    // Pop any remaining operators from the stack
    while (s->top != -1)
        postfix[j++] = pop(s);
    postfix[j] = '\0'; // Null-terminate the postfix string
    return 1; // Success
}

int main()
{
    char infix[20], postfix[20];
    STACK s;
    s.top = -1;

    printf("\nRead infix expression:\n");
    scanf("%s", infix);

    if (infix_to_postfix(&s, infix, postfix))
        printf("Result: %s\n", postfix);
    else
        printf("Conversion failed due to invalid input.\n");

    return 0;
}