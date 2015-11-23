#include <stdio.h>
#include <omp.h>

int main()
{	
	int val = 10;
	#pragma omp parallel num_threads(48) firstprivate(val)
	{
		val = val+1;
		printf("val = %d\n",val);
	}
	
	return 0;
}


























































