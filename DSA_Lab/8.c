//BST

#include<stdio.h>
#include<stdlib.h>

struct node
{
    int data;
    struct node *left;
    struct node *right;
};
typedef struct node *NODE;

NODE bst(NODE root , int key)
{
    NODE temp,cur,prev;
    temp=(NODE)malloc(sizeof(struct node));

    temp->data=key;
    temp->left=NULL;
    temp->right=NULL;
    
    if (root==NULL)
        return temp;

    cur=root;
    prev=NULL;

    while(cur!=NULL)
    {
        prev=cur;
        if(key<cur->data)
            cur=cur->left;
        else
            cur=cur->right;
    }

    if(key<prev->data)
        prev->left=temp;
    else
        prev->right=temp;
    return root;
}

void preorder(NODE root)
{
    if(root!=NULL)
    {
        printf("%d\t",root->data);
        preorder(root->left);
        preorder(root->right);
    }
}

void inorder(NODE root)
{
    if(root!=NULL)
    {
        inorder(root->left);
        printf("%d\t",root->data);
        inorder(root->right);
    }
}

void postorder(NODE root)
{
    if(root!=NULL)
    {
        postorder(root->left);
        postorder(root->right);
        printf("%d\t",root->data);
    }
}

int main()
{
    NODE root=NULL;
    int item,ch,n;

    for(;;)
    {
        printf("\n1.Insert\n2.PreOrder\n3.InOrder\n4.PostOrder\n5.Exit");
        printf("\nRead Choice:\n");
        scanf("%d",&ch);

        switch(ch)
        {
            case 1:
                printf("\nEnter the number of elements to be inserted : ");
                scanf("%d", &n);
                for (int i=1; i<=n; i++)
                {
                    printf("\nRead %d item :\n", i);
                    scanf("%d",&item);
                    root=bst(root,item);
                }
                break;
            case 2:
                printf("\nPreOrder Traversal\n");
                preorder(root);
                break;
            case 3:
                printf("\nInOrder Traversal\n");
                inorder(root);
                break;
            case 4:
                printf("\nPostOrder Traversal\n");
                postorder(root);
                break;

            default:
                exit(0);
                break;
        }
    }
    return 0;
}