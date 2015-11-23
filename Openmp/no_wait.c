#include <stdio.h>
#include <omp.h>

int main()
{
	int n = 8;
	int i;
	int j;
	int val = 0;

	#pragma omp parallel num_threads(4) firstprivate(val)
	{
		#pragma omp for nowait
		for(i = 0; i < n; ++i)
		{
			val += 1;
			printf("id:%d val:%d\n", omp_get_thread_num(), val);

		}
		#pragma omp for 
		for(j = 0;j < n; ++j)
		{
			val += 100;
			printf("id:%d val:%d\n", omp_get_thread_num(), val);
		}
		
	}
}
