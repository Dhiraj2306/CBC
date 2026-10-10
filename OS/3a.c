//Message Queues (Sender)


#include <stdio.h>
#include <sys/ipc.h>
#include <sys/msg.h>

struct msg 
{
    long type ;
    char text [100];
};

void main ()
{
    key_t key = ftok("msgfile",65);
    int msgid = msgget(key,0666|IPC_CREAT);
    
    struct msg message;
    message.type=1;
    
    printf("Enter Message");
    
    fgets(message.text,sizeof(message.text),stdin);
    msgsnd(msgid,&message,sizeof(message.text),0);
    
    printf("Message sent");
}