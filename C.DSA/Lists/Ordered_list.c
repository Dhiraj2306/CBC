 #include <stdio.h>
 #include <stdlib.h>

struct node
{
    int data;
    struct node *addr;
};
typedef struct node *NODE;  

 NODE ord_list(NODE start, int item)
 {
    NODE temp, cur, prev;
    temp=(NODE)malloc(sizeof(struct node));
    temp->data=item;
    temp->addr=NULL;

    if(start==NULL)
    {
        return temp;
    }
    
    if(item<start->data)
    {
        temp->addr=start;
        return temp;
    }

    prev=NULL;
    cur=cur->addr;
    while(cur!=NULL && item > cur->data)
    {
        prev=cur;
        cur=cur->addr;
    }
    prev->addr=temp;
    temp->addr=cur;
    return start;
 }