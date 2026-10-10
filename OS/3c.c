//Shared Memory (writer)

#include <stdio.h>
#include <sys/ipc.h>
#include <sys/shm.h>

void main ()
{
    key_t key=ftok("shmfile",65);
    int shmid= shmget(key,1024,0666|IPC_CREAT);
    char *data = (char*)shmat(shmid,NULL,0);
    
    printf("Enter data to write : ");
    fgets(data,1024,stdin);
    
    printf("Data written to shared memory \n");
    shmdt(data);
}