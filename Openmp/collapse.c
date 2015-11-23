#include <stdio.h>
#include <omp.h>

int main()
{
	int n = 4;
	int i;
	int j;
	int val = 0;

	#pragma omp parallel num_threads(4) 
	{
		#pragma omp for collapse(2) firstprivate(val)
		for(i = 0; i < n; ++i)
		{
			for(j = 0; j < n; ++j)
			{
				val += 1;
				printf("id:%d\tval:%d\n",omp_get_thread_num(),val);
			}
		}	
	}
	
	return 0;
}


