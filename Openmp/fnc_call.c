#include <stdio.h>
#include <omp.h>

void foo();

int main()
{	
	int val = 1;
	#pragma omp parallel num_threads(4) firstprivate(val)
	{
		val = val+1;
		printf("val = %d\n",val);
		foo();
	}
	
	return 0;
}

void foo()
{
	int z = 100;
	printf("In foo function\n");
}




