#include<stdio.h>

int main()
{
	int a = 30;
	int b = 20; 

	while(a!=b)
	{
		if(a>b)
			a=a-b;
		else
			b=b-a;
	}

	printf("GCD=%d\n",a);

	return 0;
}
