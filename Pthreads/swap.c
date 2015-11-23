#include <stdio.h>
#include <pthread.h>
#define NT 4
#define N 16

pthread_t t[NT];

void* swap(void* ptr)
{
	int* a = (int *)ptr;
	int i;
	

	for(i=0;i<NT;i+=2)
	{
		int temp = a[i];
		a[i] = a[i+1];
		a[i+1] = temp;
	}
}


int main()
{	
	int i;
	int a[] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
	int offset = 0;

	for(i=0;i<NT;++i)	
	{
		pthread_create(&t[i],0,swap,a+offset);
		offset += 4;
	}
	
	for(i=0;i<NT;++i)	
	{
		pthread_join(t[i],0);	
	}

	return 0;
}

