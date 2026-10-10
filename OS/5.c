//Simulate the following CPU scheduling algorithm using C Programming: i) FCFS

#include <stdio.h>


void inputProcess(int n, int at[], int bt[], int pid[])
{
	for (int i = 0; i < n; i++)
	{
		printf("\nEnter AT and BT for process P[%d]", i+1);
		scanf("%d %d", &at[i], &bt[i]);
		pid[i]= i+1;
	}
}


void sortbyArrivalTime(int n, int at[], int bt[], int pid[])
{
	int temp;
	for(int i=0; i < n-1; i++)
	{
		for(int j = i+1; j < n; j++)
		{
			if (at[i] > at[j])
			{
				temp=at[i]; //swap AT
				at[i]=at[j];
				at[j]=temp;
				
				temp=bt[i]; //swap BT
				bt[i]=bt[j];
				bt[j]=temp;
				
				temp=pid[i]; //swap pid
				pid[i]=pid[j];
				pid[j]=temp;
				
			}
		}
	}
}



void calculateTime(int n, int at[], int bt[], int ct[], int tat[], int wt[], int start_time[],int pid[], int *total_tat, int *total_wt)
{
	for (int i = 0; i < n; i++)
	{
		if (i==0)
			start_time[i] = at[i]>0 ? at[i] : ct[i-1];
		else
			start_time[i] = (at[i] > ct[i-1])  ? at[i] : ct[i-1];
		ct[i] = start_time[i] + bt[i];
		tat[i] = ct[i] - at[i];
		wt[i] = tat[i] - bt[i];
		*total_tat += tat[i];
		*total_wt += wt[i]; 
	}
}


void displayTable(int n, int pid[], int at[], int bt[], int ct[], int tat[], int wt[])
{
	printf("\nProcess\tAT\tBT\tCT\tTAT\tWT\n");
	for(int i=0; i<n; i++)
	{
		printf("P[%d]\t%d\t%d\t%d\t%d\t%d\n", pid[i], at[i], bt[i], ct[i], tat[i], wt[i]);
	}
}


void displayGanttChart(int n, int pid[], int start_time[], int ct[])
{
	printf("\n\nGantt Chart : \n");
	for (int i=0; i<n; i++)
		printf("---------");
		
	printf("-\n|");
	for (int i=0; i<n; i++)
		printf("  P[%d]  |", pid[i]);
		
	printf("\n  ");
	for (int i=0; i<n; i++)
		printf("---------");
		
	printf("-\n");
	printf("%d", start_time[0]);
	for (int i=0; i<n; i++)
		printf("   %d", ct[i]);
		
	printf("\n");
}



int main ()
{
	int n, i;
	int at[20], bt[20], ct[20], tat[20], wt[20], start_time[20], pid[20];
	int total_tat = 0,  total_wt = 0;
	
	printf("\nEnter the number of processes : ");
	scanf("%d", &n);
	
	inputProcess(n, at, bt, pid);
	sortbyArrivalTime(n, at, bt, pid);
	calculateTime(n, at, bt, ct, tat, wt, start_time, pid, &total_tat, &total_wt);
	displayTable(n, pid, at, bt, ct, tat, wt);
	
	printf("\nAvg TAT = %.2f\n", (float)total_tat);
	printf("\nAvg WT = %.2f\n", (float)total_wt);
	
	displayGanttChart(n, pid, start_time, ct);
	return 0;
}