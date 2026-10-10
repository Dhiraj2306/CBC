#include <stdio.h>
#include <stdlib.h>

int gcd(int a, int b)
{
    if(b==0)
        return a;
    return gcd(b,a%b);
}

int main ()
{
    int a,b;
    printf("\n read values for a and b: ");
    scanf("%d %d",&a,&b);
    printf("\n GCD of %d and %d is %d\n", a,b,gcd(a,b));
    return 0;
}