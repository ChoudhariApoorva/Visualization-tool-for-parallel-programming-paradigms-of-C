#include <stdio.h>

int g = 100;

int main()
{
	int* p;
	int a = 100;
	p = &a;
	printf("ptr p  = %d\n",*p);
	return 0;
}
