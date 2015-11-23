#include <stdio.h>

void bubble_sort(int *,int);

int main()
{	
	int a[] = {5,3,4,2,1};
	int n = 5;
	int i = 0;
	bubble_sort(a,n);
	
	for(i=0;i<n;++i)
		printf("%4d\n",a[i]);
	return 0;
}

void bubble_sort(int a[],int n)
{
	int i,j,temp;
	
	for(i=0;i<n-1;++i)
	{
		for(j=i+1;j<n;++j)	
		{
			if(a[i] > a[j])		
			{
				temp = a[i];
				a[i] = a[j];
				a[j] = temp;			
			}
		}
	}
}



