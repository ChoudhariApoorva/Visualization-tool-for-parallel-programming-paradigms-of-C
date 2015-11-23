#include <stdio.h>
#include <omp.h>

int main()
{
	int i;
	int n = 4;
	int sum = 0;
	int a[] = {1,2,3,4};

	#pragma omp parallel num_threads(4) private(i) 
	{
		#pragma omp for reduction(+:sum)
		for(i=0;i<n;++i)
		{
			sum += a[i];
			printf("Thread id=%d sum=%d\n",omp_get_thread_num(),sum);
		}
	}

	printf("sum = %d\n",sum); 

	return 0;
}


