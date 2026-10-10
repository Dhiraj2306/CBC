#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <math.h>
#define SIZE 10

struct stack
{
    int top;
    int data[SIZE];
};
typedef struct stack STACK;

void push(STACK *s, char item)
{
    s->data[++(s->top)]=item;
}

char pop(STACK *s)
{
    return s->data[(s->top)--];
}

void dec_to_binary(STACK *s, int num)
{
    int r, bin[10], i=0, j;

    while (num!=0) 
    {
        r=num%2;
        push(s,r);
        num/=2;
    }
    while (s->top!=0)
    {
        bin[i++]=pop(s);
    }
    printf("The binary equi is : ");
    for (j=0; j<i; j++)
    {
        printf("%d", bin[j]);
    }
}
int main ()
{
    int num;
    printf("\nEnter the number : ");
    scanf("%d",num);
    dec_to_binary(&s,num);
}