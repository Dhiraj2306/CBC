//Simulate Deadlock Avoidance through Banker's Safety Algorithm

#include <stdio.h>
#include <stdbool.h>
#define MAX 10

int n, m;
int alloc[MAX][MAX], max[MAX][MAX], need[MAX][MAX], avail[MAX];
int finish[MAX] = {0}, safeSeq[MAX];

void inputMatrices() 
{
    printf("Enter number of processes: ");
    scanf("%d", &n);

    printf("Enter number of resource types: ");
    scanf("%d", &m);

    printf("\nEnter Allocation Matrix:\n");
    for (int i = 0; i < n; i++) 
    {
        printf("Process %d: ", i);
        for (int j = 0; j < m; j++) 
        {
            scanf("%d", &alloc[i][j]);
        }
    }

    printf("\nEnter Maximum Matrix:\n");
    for (int i = 0; i < n; i++) 
    {
        printf("Process %d: ", i);
        for (int j = 0; j < m; j++) 
        {
            scanf("%d", &max[i][j]);
            need[i][j] = max[i][j] - alloc[i][j];
        }
    }

    printf("\nEnter Available Resources: ");
    for (int i = 0; i < m; i++) 
    {
        scanf("%d", &avail[i]);
    }
}

bool isSafeState() {
    int work[MAX];
    for (int i = 0; i < m; i++) 
    {
        work[i] = avail[i];
    }

    int count = 0;
    while (count < n) 
    {
        bool found = false;

        for (int i = 0; i < n; i++) 
        {
            if (!finish[i]) 
            {
                bool canRun = true;

                for (int j = 0; j < m; j++) 
                {
                    if (need[i][j] > work[j]) 
                    {
                        canRun = false;
                        break;
                    }
                }

                if (canRun) 
                {
                    for (int k = 0; k < m; k++)
                        work[k] += alloc[i][k];

                    safeSeq[count++] = i;
                    finish[i] = 1;
                    found = true;
                }
            }
        }

        if (!found)
            return false;
    }

    return true;
}

void printResult(bool safe) 
{
    if (safe) 
    {
        printf("\nSystem is in a safe state.\nSafe sequence: ");
        for (int i = 0; i < n; i++)
            printf("P%d ", safeSeq[i]);
        printf("\n");
    } 
    else 
    {
        printf("\nSystem is NOT in a safe state. No safe sequence found.\n");
    }
}

int main() 
{
    inputMatrices();
    bool safe = isSafeState();
    printResult(safe);
    return 0;
}
