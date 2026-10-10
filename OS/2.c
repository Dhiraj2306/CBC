//Implement the wait(), exit() and abort() system call using C programming


#include <stdio.h>
#include <stdlib.h> //exit() and abort()
#include <unistd.h> //fork() and getpid()
#include <sys/wait.h> //All wait system calls
#include <sys/types.h> //pid_t

int main ()
    {
        pid_t pid1, pid2;
        int status;


        pid1=fork();

        if (pid1<0)
        {
            perror("Fork Failed");
            return 1;
        }
        else if (pid1 == 0)
        {
            printf("child1 (PID % d) : exiting normally with code 10 \n",getpid());
            exit(10);
        }	

        wait(&status);

        if(WIFEXITED(status))
        {
            printf("Parent : child1 exited with code %d \n",WEXITSTATUS(status));
        }
        


        pid2=fork();

        if (pid2<0)
        {
            perror("Fork Failed");
            return 1;
        }
        else if (pid2 == 0)
        {
            printf("child2 (PID % d) : aborting the process \n",getpid());
            abort();
        }	

        wait(&status);
            
        if(WIFSIGNALED(status))
        {
            printf("Parent : child2 terminated by signal %d\n",WTERMSIG(status));
        }
        
        

        printf("Parent : done\n");
        return 0;
    }