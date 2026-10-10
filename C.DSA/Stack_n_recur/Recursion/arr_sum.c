#include <stdio.h>
#include <stdlib.h>

int arr_sum(int a[10], int n)
{
    if (n==0)return a[0];
    return arr_sum(a,n-1);
}

int main ()
{
    int n, a[10];
} 