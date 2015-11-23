#include <stdio.h>
#include <pthread.h>

void* foo(void*);

pthread_t t;	

int main()
{
	int a = 10;
	pthread_create(&t, 0, foo, 0);
	printf("a = %d\n",a);
	pthread_join(t,0);
	return 0;
}

void* foo(void* ptr)
{
	int val = 100;
	int val2 = 200;
	printf("val = %d\n",val);
}




