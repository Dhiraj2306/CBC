#include <stdio.h>
#include <stdlib.h>

int max(int a, int b)
{
    if(a > b)
        return a;
    else
        return b;
}

int main()
{
    int n, W, w[10], P[10], i, j, V[10][10], x[10] = {0};

    printf("\nRead number of objects: ");
    scanf("%d", &n);

    printf("\nRead knapsack capacity: ");
    scanf("%d", &W);

    printf("\nRead weights of objects\n");
    for(i = 1; i <= n; i++)
        scanf("%d", &w[i]);

    printf("\nRead profit of objects\n");
    for(i = 1; i <= n; i++)
        scanf("%d", &P[i]);

    for(i = 0; i <= n; i++)
    {
        for(j = 0; j <= W; j++)
        {
            if(i == 0 || j == 0)
                V[i][j] = 0;

            else if(j - w[i] < 0)
                V[i][j] = V[i-1][j];

            else
                V[i][j] = max( ( V[i-1][j] ) , ( V[i-1][j-w[i]] + P[i] ) );

            printf("%d\t", V[i][j]);
        }
        printf("\n");
    }

    i = n;
    j = W;

    while(i != 0 && j != 0)
    {
        if(V[i][j] != V[i-1][j])
        {
            x[i] = 1;
            j = j - w[i];
        }
        i = i - 1;
    }

    printf("\nObject\tWeight\tProfit\n");

    for(i = 1; i <= n; i++)
    {
        if(x[i] == 1)
            printf("%d\t%d\t%d\n", i, w[i], P[i]);
    }

    return 0;
}