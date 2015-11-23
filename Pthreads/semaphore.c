#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

pthread_t t1;
pthread_t t2;
sem_t sem;

void* f1(void* ptr)
{
	char* s = (char*)ptr;
	while(*s)
	{
		sem_wait(&sem);
		printf("%c\n",*s);
		++s;
		sem_post(&sem);
	}
}

int main()
{
	sem_init(&sem, 0, 1);
	pthread_create(&t1, 0, f1, "abcdefgh");
	pthread_create(&t2, 0, f1, "ABCDEFGH");	
	pthread_join(t1, 0);
	pthread_join(t2, 0);
	sem_destroy(&sem);
}

