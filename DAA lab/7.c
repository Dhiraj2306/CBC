#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define SIZE 256

int table[SIZE];

void shift_table(char P[])
{
    int i, m;
    m = strlen(P);

    for(i = 0; i < SIZE; i++)
        table[i] = m;

    for(i = 0; i <= m - 2; i++)
        table[P[i]] = m - 1 - i;
}

int Horspool(char T[], char P[])
{
    int i, m, n, k;

    n = strlen(T);
    m = strlen(P);

    shift_table(P);

    i = m - 1;

    while(i <= n - 1)
    {
        k = 0;

        while((k < m) && T[i - k] == P[m - 1 - k])
            k++;

        if(k == m)
            return i - m + 1;
        else
            i = i + table[T[i]];
    }

    return -1;
}

int main()
{
    char P[10], T[50];
    int pos = -1;

    printf("\nRead text:\n");
    scanf("%s", T);

    printf("\nRead pattern:\n");
    scanf("%s", P);

    pos = Horspool(T, P);

    if(pos == -1)
        printf("\nPattern not found");
    else
        printf("\nPattern found at location : %d", pos);

    return 0;
}