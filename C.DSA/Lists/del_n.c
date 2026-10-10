#include <stdio.h>
#include <stdlib.h>

struct node
{
    int data;
    struct node *addr;
};
typedef struct node *NODE;  

NODE del_n(NODE start, int pos)
{
    NODE temp, prev, cur;
    int count = 1;

    if (pos==1)
    {
        temp=start;
        start=start->addr;

        printf("\nNode deleted is %d", temp->data);
        free(temp);

        return start;
    }

    prev=NULL;
    cur=start;

    while(cur != NULL && pos != count)
    {
        prev=cur;
        cur=cur->addr;
        count++;
    }
    if (pos != count)
    {
        printf("\nNode not found");
        return start;
    }
    prev->addr = cur->addr;
    printf("\nNode deleted is %d", cur->data);
    free(cur);
    return start;
}