#include <stdio.h>
#include <omp.h>

int main()
{
	int tid = 0;

	#pragma omp parallel num_threads(4) firstprivate(tid)
	{
		tid = omp_get_thread_num();
		printf("Thread id = %d\n",tid);
			
		#pragma omp master
		{
			printf("Only master thread\n");			
		}
	}
}


