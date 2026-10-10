//5.

#include <stdio.h>
#define SIZE 5

struct queue
{
    int r,f;
    int data[SIZE];
};
typedef struct queue QUEUE;

void enqueue(QUEUE *q, int item)
{
    if (q->r==SIZE-1)
        printf("\nQueue full");

        else
        {

            q->data[++(q->r)]=item;

            if (q->f==-1)
                q->f=0;
        }
}

void dequeue (QUEUE *q)
{
    if (q->f==-1)
        printf("\nQueue empty");

        else
        {
            printf("\nDeleted item is %d", q->data[q->f]);
            if (q->f==q->r)
                q->f=q->r=-1;
            else
                q->f++;
        }
}

void display (QUEUE q)
{
    int i;
    if (q.f==-1)
        printf("\nQueue empty");

        else
        {
            printf("\nQueue elements are:\n");
            for (i=q.f; i<=q.r; i++)
                printf("%d\t", q.data[i]);
        }
}

int main()
{
    int item, ch;
    QUEUE q;
    q.f=q.r=-1;

    while(1)
    {
        printf("\n1.Enqueue\n2.Dequeue\n3.Display\n4.Exit\nEnter your choice: ");
        scanf("%d", &ch);

        switch (ch)
        {
            case 1: printf("\nEnter the item to be inserted: ");
                    scanf("%d", &item);
                    enqueue(&q, item);
                    break;

            case 2: dequeue(&q);
                    break;

            case 3: display(q);
                    break;

            case 4: return 0;

            default: printf("\nInvalid choice");
        }
    }
}