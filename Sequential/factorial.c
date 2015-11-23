#include<stdio.h>

int fact(int);

int main()
{
	int num = 5;

	int f = fact(num);
	
	printf("Factorial of %d is = %d\n",num,f);

	return 0;
}

int fact(int x)
{
	if(x == 1 || x == 0)
		return 1;
	else 
		return x * fact(x-1);
}

 


















