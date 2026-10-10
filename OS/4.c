//Simulate solutions to Producer – Consumer Process Synchronization Problems using C Programming

#include <stdio.h>
#include <stdlib.h>
#define BUFFERSIZE 10

int mutex = 1;
int full = 0;
int empty, n, item1, item2;
int buffer[BUFFERSIZE];
int in=0, out=0;

void wait(int *s)
{
    (*s)--;
}

void signal(int *s)
{
    (*s)++;
}

void producer ()
{
    if ((in-out)>=n)
    {
        printf("Can not add item buffer full");
        return;
    }


    wait(&empty);
    wait(&mutex);

    printf("\nEnter an item : ");
    scanf("%d", &item1);
    
    buffer[in % BUFFERSIZE] = item1;
    in++;

    signal(&mutex);
    signal(&full);
}

void consumer()
{
    if (out>=in)
    {
        printf("\nNo item to consume");
        return;
    }
    
    wait(&full);
    wait(&mutex);
    
    item2=buffer[out % BUFFERSIZE];
    printf("\nConsumed item is : %d", item2);
    out++;

    signal(&mutex);
    signal(&empty);
}

int main ()
{
    int choice;
    printf("Enter the no. of items (n) : ");
    scanf("%d",&n);
    
    if (n>BUFFERSIZE)
    {
        printf("Buffer size exceeded max allowed is %d", BUFFERSIZE);
        return 1;
    }
    
    empty=n;
    
    while(1)
    {
        printf("\n1.Producer\n2.Consumer\n3.Exit\nEnter your choice : ");
        scanf("%d",&choice);
        
        switch(choice)
        {
            case 1: 
                producer();
                break;
            case 2: 
                consumer();
                break;
            case 3: 
                exit(0);
                break;
            default:
                printf("\nInvalid choice");
        }
    }
    return 0;
}