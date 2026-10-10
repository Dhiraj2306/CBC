#include <stdio.h>
#include <stdlib.h>

struct node
{
    int data;
    struct node *addr;
};
typedef struct node *NODE;  

NODE ins_n(NODE start, int pos, int item)
{
    NODE temp, prev, cur;
    int i;

    temp=(NODE)malloc(sizeof(struct node));
    temp->data=item;
    temp->addr=NULL;

    if (pos==1)
    {
        temp->addr=start;
        return temp;
    }

    prev=NULL;
    cur=start;

    for (i = 1; i < pos; i++)
    {
        if (cur == NULL)
        {
            printf("Invalid position\n");
            return start;
        }
        prev = cur;
        cur = cur->addr;
    }

    temp->data=item;
    prev->addr=temp;
    temp->addr=cur;
    return start;

}