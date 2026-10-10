 #include <stdio.h>
 
 #include <stdlib.h>

struct node
{
    int data;
    struct node *addr;
};
typedef struct node *NODE;  

NODE reverse(NODE start)
{
    NODE temp, prev, cur;

    if(start->addr == NULL)
        return temp;
    
    temp=NULL;
    prev=NULL;
    cur=start;
    while(cur!=NULL)
    {
        temp=prev;
        prev=cur;
        cur=cur->addr;
        prev->addr=temp;
    }
    return prev;
}