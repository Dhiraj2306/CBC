#include <stdio.h>
#include <stdlib.h>

int n, d, w[10], x[10];

void SOS(int s, int k, int r)
{
    int i;
    static int count = 1;

    x[k] = 1;

    if((s + w[k]) == d)
    {
        printf("\nSolution %d : ", count++);

        for(i = 1; i <= k; i++)
        {
            if(x[i] == 1)
                printf("%d\t", w[i]);
        }
        printf("\n");
    }

    else if((s + w[k] + w[k + 1]) <= d)
    {
        SOS(s + w[k], k + 1, r - w[k]);
    }

    if((s + r - w[k] >= d) && (s + w[k + 1] <= d))
    {
        x[k] = 0;
        SOS(s, k + 1, r - w[k]);
    }
}

int main()
{
    int i, sum = 0;

    printf("\nRead number of elements: ");
    scanf("%d", &n);

    printf("\nRead elements in ascending order:\n");
    for(i = 1; i <= n; i++)
    {
        scanf("%d", &w[i]);
        sum = sum + w[i];
    }

    printf("\nRead value of d: ");
    scanf("%d", &d);

    SOS(0, 1, sum);

    return 0;
}