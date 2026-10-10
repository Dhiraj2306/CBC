int isMatchingPair(char open, char close) {
    if (open == '(' && close == ')') return 1;
    if (open == '{' && close == '}') return 1;
    if (open == '[' && close == ']') return 1;
    return 0;
}

#define MAX 100

int isValidParenthesis(char expr[]) {
    char stack[MAX];
    int top = -1;
    int i = 0;

    while (expr[i] != '\0') {
        // Push opening brackets
        if (expr[i] == '(' || expr[i] == '{' || expr[i] == '[') {
            stack[++top] = expr[i];
        }
        // Pop and match closing brackets
        else if (expr[i] == ')' || expr[i] == '}' || expr[i] == ']') {
            if (top == -1)
                return 0;  // Stack empty → invalid

            if (!isMatchingPair(stack[top], expr[i]))
                return 0;  // Mismatch

            top--;
        }
        i++;
    }

    // If stack is empty → valid
    return (top == -1);
}


