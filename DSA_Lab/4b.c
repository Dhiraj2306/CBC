#include <stdio.h>
#include <stdlib.h>

void TOH(int n, char s, char d, char t)
{
    if (n > 1)
    {
        TOH(n - 1, s, t, d);
        printf("Move disk %d from rod %c to rod %c\n", n,s,d);
        TOH(n - 1, t, d, s);
    }
    else
    {
        printf("Move disk 1 from rod %c to rod %c\n", s, d);
    }
}

int main()
{
    int n;
    printf("Enter the number of disks: ");
    scanf("%d", &n);
    TOH(n, 'S', 'D', 'T');
    return 0;
}