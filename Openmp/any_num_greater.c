#include <stdio.h>
#include <omp.h>
#include <stdlib.h>

int num_greater(int n)
{
	return (n>100)?1:0;
}

int main()
{
	int a[] = {11,22,33,414};
	int n = 4;
	int i;
	int res = 0;

	#pragma omp parallel shared(res)
	{
		#pragma omp for
		for(i=0;i<n;++i)	
		{
			if(num_greater(a[i]))
				res = 1;
		}
	}
	
	if(res)
		printf("Satisfies condition\n");
	else
		printf("Does not satisfy condition\n");

	return 0;
}
