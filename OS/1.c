//Implement the fork() and exec() system call using C programming

#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main ()
{
    pid_t pid;
    pid = fork();
    
    if (pid<0)
    {
        perror("Fork Failed");
        return 1;
    }
    
    else if (pid == 0)
    {
        printf("\nChild process completed");
        execl("/bin/date","date",NULL);
    }
    
    else 
    {
        printf("\nParent process waiting");
        wait(NULL);
        printf("\nChild completed\n");
    }
    return 0;  
}