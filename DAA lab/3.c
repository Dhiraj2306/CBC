#include <stdio.h>
#include <stdlib.h>

int count = 0;

int partition(int A[10], int l, int r)
{
    int i, j, pivot, temp;

    pivot = A[l];
    i = l + 1;
    j = r;

    while(1)
    {
        while(pivot >= A[i] && i <= r)
        {
            i++;
            count++;
        }

        while(pivot < A[j])
        {
            j--;
            count++;
        }

        if(i < j)
        {
            temp = A[i];
            A[i] = A[j];
            A[j] = temp;
        }
        else
        {
            temp = A[l];
            A[l] = A[j];
            A[j] = temp;

            return j;
        }
    }
}

void quicksort(int A[10], int l, int r)
{
    int s;

    if(l < r)
    {
        s = partition(A, l, r);

        quicksort(A, l, s - 1);
        quicksort(A, s + 1, r);
    }
}

int main()
{
    int A[10], n, i;


    printf("\nNo of elements: ");
    scanf("%d", &n);


    printf("Enter elements\n");
    for(i = 0; i < n; i++)
    {
        scanf("%d", &A[i]);
    }

    
    quicksort(A, 0, n - 1);


    printf("Sorted elements:\n");
    for(i = 0; i < n; i++)
    {
        printf("%d ", A[i]);
    }


    printf("\nNo of comparisons: %d", count);


    return 0;
}