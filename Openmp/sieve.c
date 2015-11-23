#include <stdio.h>
#include <omp.h>

int main()
{
	int n = 16;
	int a[16];
	int i,j;

	#pragma omp parallel private(i)
	{
		#pragma omp for
		for(i=2;i<=n;++i)	
			a[i] = i;
	}	
	
	#pragma omp for private(i,j)
	for(i=2;i<=n;++i)
	{
		for(j=i+i;j<=n;j+=i)	
			a[j] = 0;
	}
	
	for(i=2;i<=n;++i)
		if(a[i])
			printf(" %d\n",a[i]);

	return 0;
}

