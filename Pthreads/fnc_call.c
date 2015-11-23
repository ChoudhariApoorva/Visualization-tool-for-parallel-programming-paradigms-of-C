#include <stdio.h>
#include <pthread.h>

pthread_t t;
pthread_t  t1;

void test()
{
	int q = 10;
	int r = 20;
}

void bar()
{
	int temp = 200;
	printf("In function bar\n");
	test();
}

void* foo(void* ptr)
{
	int val = 300;
	printf("ptr = %d\n",*(int*)ptr);
	bar();
}

int main()
{
	int n = 100;
	pthread_create(&t, 0, foo, &n);
	pthread_create(&t1,0,foo,&n);
	pthread_join(t, 0);
	pthread_join(t1,0);
	return 0;
}



