#include<stdio.h>

int gcd(int,int);

int main()
{
	int a = 5;
	int b = 20; 

	int g = gcd(a,b);
	
	printf("GCD = %d\n",g);

	return 0;
}

int gcd(int x,int y)
{
	while(x!=y)
	{
		if(x>y)
			x=x-y;
		else
			y=y-x;
	}
	
	return x;
}



























