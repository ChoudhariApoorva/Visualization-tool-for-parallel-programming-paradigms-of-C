#include <stdio.h>
#include <omp.h>

void fn1()
{
	printf("In fn1\n");
}

void fn2()
{
	printf("In fn2\n");
}

void fn3()
{
	printf("In fn3\n");
}

int main()
{
	int a = 10; 
	#pragma omp parallel num_threads(3)	
	{
		#pragma omp sections
		{
			fn1();
			#pragma omp section
			{
				fn2();			
			}	
			#pragma omp section
			{
				fn3();
			}
		}	
	}
	return 0;
}

