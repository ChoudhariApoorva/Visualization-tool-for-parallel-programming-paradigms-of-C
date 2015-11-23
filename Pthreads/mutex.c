#include <stdio.h>
#include <pthread.h>

pthread_t t1;
pthread_t t2;
pthread_mutex_t m;

void* f1(void* ptr)
{
	char* s = (char*)ptr;
	pthread_mutex_lock(&m);
	while(*s)
	{	
		printf("%c\n",*s);
		++s;
	}
	pthread_mutex_unlock(&m);
}
int main()
{
	pthread_mutex_init(&m, 0);
	pthread_create(&t1, 0, f1, "abcdefgh");
	pthread_create(&t2, 0, f1, "ABCDEFGH");
	pthread_join(t1, 0);
	pthread_join(t2, 0);
	pthread_mutex_destroy(&m);
}

