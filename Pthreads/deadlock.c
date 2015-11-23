#include <stdio.h>
#include <pthread.h>

pthread_t t1;
pthread_t t2;
pthread_mutex_t m1;
pthread_mutex_t m2;

void* f1(void* ptr)
{
	char* s = (char*)ptr;
	pthread_mutex_lock(&m1);
	while(*s)
	{	
		printf("%c\n",*s);
		++s;
	}
	pthread_mutex_lock(&m2);
	printf("Unlock in f1\n");
}
void* f2(void* ptr)
{
	char* s = (char*)ptr;
	pthread_mutex_lock(&m2);
	while(*s)
	{	
		printf("%c\n",*s);
		++s;
	}
	pthread_mutex_lock(&m1);
	printf("Unlock in f2\n");
}

int main()
{
	pthread_mutex_init(&m1, 0);
	pthread_mutex_init(&m2, 0);
	pthread_create(&t1, 0, f1, "ab");
	pthread_create(&t2, 0, f2, "AB");
	pthread_join(t1, 0);
	pthread_join(t2, 0);
	pthread_mutex_destroy(&m1);
	pthread_mutex_destroy(&m2);
}


