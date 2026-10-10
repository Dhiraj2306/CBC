#include <stdio.h>
#include <stdlib.h>

int fact (int n)
{
    if (n==0 || n==-1)
        return 1;
    return n * fact(n-1); 
}

int main ()
{
    int a;
    printf("Enter number :");
    scanf("%d",a);
    printf("%d", fact(a));
    return 0;
}