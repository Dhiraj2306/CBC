//1.

#include <stdio.h>
#include <stdlib.h>
#define SIZE 5

struct stack
{
    int top;
    int data[SIZE];
};
typedef struct stack STACK;

void push(STACK *s, int item)
{
    if (s->top == SIZE-1)
        printf("\nStack overflow");
    else
        s->data[++(s->top)]=item;
}

void pop (STACK *s)
{
    if (s->top==-1)
        printf("\nStack underflow");
    else
        printf("\nelement poped is %d", s->data[(s->top)--]);
}

void display(STACK s)
{
    int i;

    if (s.top==-1)
        printf("\nStack is empty");
    else
    {
        printf("\nStack content are\n");
        for (i=s.top; i>=0; i--)
            printf("%d\n", s.data[i]);
    }
}

int main()
{
    int ch, item;
    STACK s;
    s.top=-1;
    for(;;)
    {
        printf("\n1.Push");
        printf("\n2.Pop");
        printf("\n3.Display");
        printf("\n4.Exit");
        printf("\nEnter your choice : ");
        scanf("%d",&ch);

        switch(ch)
        {
            case 1:
                printf("\nEnter the element to be pushed : ");
                scanf("%d",&item);
                push(&s,item);
                break;
            case 2:
                pop(&s);
                break;
            case 3:
                display(s);
                break;
            case 4: 
                exit(0);
                break;
            default:
                printf("\nInvalid choice");
        }
    }
    return 0;
}