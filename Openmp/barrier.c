#include <stdio.h>
#include <omp.h>

int main()
{
	int val = 0;
	int final = 0;

	#pragma omp parallel num_threads(4) firstprivate(final)
	{	
		 val += 1;

		 #pragma omp barrier
		 final = val;
		 printf("final = %d Id = %d\n",final,omp_get_thread_num());
		 	 
	} 
}





