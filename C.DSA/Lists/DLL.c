#include <stdio.h>
#include <stdlib.h>


struct node
{
    int data;
    struct node *next;
    struct node *prev;
};
typedef struct node *NODE;  


NODE insertbegin(NODE start, int item)
{
    NODE temp;
    temp=(NODE)malloc(sizeof(struct node));
    temp->data=item;
    temp->next=NULL;
    temp->prev=NULL;
    
    if(start==NULL)
        return NULL;

    temp->next=start;
    start->prev=temp;
    return temp;
}


NODE insertbegin(NODE start, int item)
{
    NODE temp, cur;
    temp=(NODE)malloc(sizeof(struct node));
    temp->data=item;
    temp->next=NULL;
    temp->prev=NULL;
    
    if(start==NULL)
        return NULL;

    cur=start;
    while(cur->next!=NULL)
        cur=cur->next;
    cur->next=temp;
    temp->prev=cur;
    return start;
}


NODE deletebegin(NODE start)
{
    NODE temp;
    if(start==NULL)
    {
        printf("\nList empty");
        return NULL;
    }
    if(start->next == NULL)
    {
        printf("\nNode del is %d", start->data);
        free(start);
        return NULL;
    }
    temp=start;
    start=start->next;
    start->prev=NULL;
    printf("\nNode del is %d", temp->data);
    free(temp);
    return start;
}


NODE deletebegin(NODE start)
{
    NODE temp, cur;
    if(start==NULL)
    {
        printf("\nList empty");
        return NULL;
    }
    if(start->next == NULL)
    {
        printf("\nNode del is %d", start->data);
        free(start);
        return NULL;
    }
    
    cur=start;
    while(cur->next != NULL)
        cur=cur->next;
    temp=cur->prev;
    temp->next=NULL;
    printdf("\nNode del is %d", cur->data);
    free(cur);
    return start;
}


void diaplay(NODE start)
{
    NODE temp;
    if (start==NULL)
        printf("\nList is empty");
    else 
    {
        printf("\nList content are : ");
        temp=start;
        while(temp!=NULL)
        {
            printf("%d\t", temp->data);
            temp=temp->data;
        }
    }
}