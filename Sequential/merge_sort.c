#include <stdio.h>

void sort(int*,int);
void merge(int*,int*,int*,int,int);

int main()
{
	int a[5];
	int n = 5;
	int i = 0;

	for(i=0;i<n;++i)
	{
		a[i] = rand()%100;
	}

	sort(a,n);
		
	for(i=0;i<n;++i)
	{
		printf(" %d \n",a[i]);
	}
		
	return 0;
}

void sort(int* a,int n)
{
	int n1 = n/2;
	int n2 = n-n1;
	int b[n1];
	int c[n2];
	int i,j;
	
	if(n > 1)
	{
		for(i=0;i<n1;++i)	
		{
			b[i]=a[i];
		}
		for(j=0;j<n2;++j)	
		{
			c[j]=a[j+n1];
		}

		sort(b,n1);
		sort(c,n2);
		
		merge(b,c,a,i,j);
	}
}
void merge(int* b,int* c,int* a,int p,int q)
{
	int i = 0;
	int j = 0;
	int k = 0;
	
	while(i<p && j<q)
	{
		if(b[i] < c[j])	
		{
			a[k] = b[i];
			++i;		
		}
		else
		{
			a[k] = c[j];	
			++j;		
		}
		++k;
	}
		
	while(i<p)
	{
		a[k] = b[i];
		++i;	
		++k;	
	}
	
	while(j<q)
	{
		a[k] = c[j];
		++j;
		++k;
	}
}









