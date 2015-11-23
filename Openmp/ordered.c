#include <stdio.h>
#include <omp.h>

int main()
{
	int n = 4;
	int i;	
	int val = 0;
	#pragma omp parallel num_threads(4) firstprivate(val)
	{
		#pragma omp for ordered
		for(i = 0; i < n; ++i)
		{
			#pragma omp ordered
			val += 1;
			printf("thread id = %d\tval = %d\n",omp_get_thread_num(),val);
		}

	}
}

