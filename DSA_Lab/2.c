#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#define SIZE 20

struct stack
{
    int top;
    int data[SIZE];
};
typedef struct stack STACK;

void push(STACK *s, int item)
{
    s->data[++(s->top)]=item;
}

char pop(STACK *s)
{
    return s->data[(s->top--)];
}

int preceed(char symbol)
{
    switch(symbol)
    {
        case '+':
        case '-':return 1;
        case '*':
        case '/':return 2;
        case '&':return 3;
    }
}

void intopost(STACK *s,char infix[20])
{
    int j=0;
    char sym,postfix[20],temp;

    for(int i=0;infix[i]!='\0';i++)
    {
        sym=infix[i];
        if (isalnum(sym))
        {
            postfix[j++]=sym;
        }
        else
        {
            switch(sym)
            {
                case '(':
                    push(s,sym);
                    break;

                case ')':
                    temp=pop(s);
                    while(temp!='(')
                    {
                        postfix[j++]=temp;
                        temp=pop(s);
                    }
                    break;
                case '+':
                case '-':
                case '*':
                case '/':
                case '^':
                    if ((s->top==-1 || (s->data[s->top])=="("))
                    {
                        push(s,sym);
                    }
                    else
                    {
                        while(preceed(s->data[s->top])>=preceed(sym) && (s->top!=1) && s->data[s->top]!='(')
                        {
                            postfix[j++]=pop(s);
                        }
                        push(s,sym);
                        break;
                    }
            }
        }
    }
    while(s->top!=-1)
    {
        postfix[j++]=pop(s);
    }
    postfix[j]='\0';
    printf("\nPostfix Expression is %s ",postfix);
}

int main()
{
    char infix[20];
    STACK s;
    s.top-=1;
    printf("\nRead the expression: ");
    scanf("%s",infix);
    intopost(&s,infix);
    return 0;
}