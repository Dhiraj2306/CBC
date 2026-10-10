#include <stdio.h>
#include <stdlib.h>

void Dijkstra(int a[10][10], int n, int s, int d[10])
{
    int i, j, visited[10], min, v, count = 1;

    for(i = 1; i <= n; i++)
    {
        visited[i] = 0;
        d[i] = a[s][i];
    }

    visited[s] = 1;
    d[s] = 0;

    while(count <= n)
    {
        min = 999;

        for(i = 1; i <= n; i++)
        {
            if(d[i] < min && visited[i] == 0)
            {
                min = d[i];
                v = i;
            }
        }

        visited[v] = 1;
        count++;

        for(i = 1; i <= n; i++)
        {
            if((d[i] > d[v] + a[v][i]) && visited[i] == 0)
            {
                d[i] = d[v] + a[v][i];
            }
        }
    }
}

int main()
{
    int i, j, a[10][10], s, d[10], n;

    printf("\nRead number of vertices: ");
    scanf("%d", &n);

    printf("\nRead Cost Matrix:\n");

    for(i = 1; i <= n; i++)
    {
        for(j = 1; j <= n; j++)
        {
            scanf("%d", &a[i][j]);

            if(a[i][j] == 0)
                a[i][j] = 999;
        }
    }

    printf("\nRead source vertex: ");
    scanf("%d", &s);

    Dijkstra(a, n, s, d);

    for(i = 1; i <= n; i++)
    {
        if(s != i)
        {
            printf("\nThe shortest path from %d to %d is %d",
                   s, i, d[i]);
        }
    }

    return 0;
}