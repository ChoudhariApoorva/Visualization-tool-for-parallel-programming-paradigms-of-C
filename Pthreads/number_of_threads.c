#include <stdio.h>
#include <pthread.h>

void* foo(void*);

pthread_t t[4];

int main()
{
	int i;
	
	for(i=0;i<4;++i)
		pthread_create(&t[i], 0, foo, 0);

	for(i=0;i<4;++i)
		pthread_join(t[i],0);

	return 0;
}

void* foo(void* ptr)
{
	int val = 100;
	printf("val = %d\n",val);
}







