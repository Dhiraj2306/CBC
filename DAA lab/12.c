#include <stdio.h>
#include <stdlib.h>

int x[20], count = 1;


int Place(int k, int i)
{
    int j;

    for(j = 1; j <= k - 1; j++)
    {
        if((x[j] == i) || (abs(x[j] - i) == abs(j - k)))
            return 0;
    }

    return 1;
}

void NQueens(int k, int n)
{
    int i, j;

    for(i = 1; i <= n; i++)
    {
        if(Place(k, i))
        {
            x[k] = i;

            if(k == n)
            {
                printf("\nSolution %d:\n\n", count++);

                for(i = 1; i <= n; i++)
                {
                    for(j = 1; j <= n; j++)
                    {
                        if(x[i] == j)
                            printf("Q\t");
                        else
                            printf("*\t");
                    }

                    printf("\n");
                }
            }
            else
            {
                NQueens(k + 1, n);
            }
        }
    }
}

int main()
{
    int n;

    printf("\nRead number of queens: ");
    scanf("%d", &n);

    NQueens(1, n);

    return 0;
}
