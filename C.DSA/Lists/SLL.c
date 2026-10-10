#include <stdio.h>
#include <stdlib.h>

struct node
{
    int data;
    struct node *addr;
};
typedef struct node *NODE;  



NODE insertbegin (NODE start, int item)
{
    NODE temp;
    temp = (NODE)malloc(sizeof(struct node));
    temp->data=item;
    temp->addr=NULL;

    if (start=NULL)
        return temp;
    temp->addr=start;
    return temp;
}



NODE insertend (NODE start, int item)
{
    NODE temp, cur;
    temp=(NODE)malloc(sizeof(struct node));
    temp->data=item;
    temp->addr=NULL;

    if (start=NULL)
        return temp;
    cur=start;

    while(cur->addr!=NULL)
        cur=cur->addr;
    cur->addr=temp;
    return start;
}



NODE deletebegin(NODE start)
{
    NODE temp;
    
    if(start==NULL)
    {
        printf("\nList is empty");
        return NULL;
    }

    if(start->addr=NULL)
    {
        printf("\nNode deleted is %d",start->data);
        free(start);
        return NULL;
    }

    temp=start;
    start=start->addr;
    printf("\nNode deleted is %d",temp->data);
    free(temp);
    return start;
}



NODE deleteend (NODE start)
{
    NODE prev, cur;

    if (start==NULL)
        printf("\nList is empty");
    
    if (start->addr==NULL)
        printf("\nNode deleted is %d", start->data);
        free(start);
        return NULL;

    prev=NULL;
    cur=start;

    while(cur->addr!=NULL)
    {
        prev=cur;
        cur=cur->addr;
    }
    prev->addr=NULL;
    printf("\nNode deleted is %d", cur->data);
    free(cur);
    return start;
}



void display(NODE start)
{
    NODE temp;

    if(start=NULL)
        printf("\nList is empty");

    else 
    {
        printf("\nList content are :");
        temp=start;

        while (temp->addr!=NULL)
        {
            printf("\n%d",temp->data);
            temp=temp->addr;
        }
    }
}


