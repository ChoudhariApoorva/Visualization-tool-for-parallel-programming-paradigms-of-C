#include <stdio.h>
#include <omp.h>

int main()
{	
	int val = 10;
	int shared_val = 100;
	#pragma omp parallel num_threads(4) firstprivate(val)
	{
		val = val+1;
		shared_val = shared_val + 1;
		printf("val = %d\n",val);
		printf("shared_val = %d\n",shared_val);
	}
	
	return 0;
}
