#include <stdio.h>
#include <omp.h>

int main()
{
	int n = 8;
	int i;
	int j;
	int x = 0;
	int y = 0;

	#pragma omp parallel num_threads(4) firstprivate(x,y)
	{
		#pragma omp for
		for(i = 0; i < n; ++i)
			x += 1;
	
		#pragma omp for 
		for(j = 0;j < n; ++j)
			y += 1;
	}
}
