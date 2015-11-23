#include <stdio.h>
#include <omp.h>

int main()
{
	int val = 0;
	int i = 0;
	int n = 8;
	
	#pragma omp parallel for private(i) firstprivate(val) schedule(dynamic)
	for(i=0;i<n;++i)
	{
		val = val+1;
		printf("Id=%d\tval=%d\n",omp_get_thread_num(),val);
	}
	
	return 0;
}

