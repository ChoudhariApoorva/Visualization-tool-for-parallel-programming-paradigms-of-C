#include <stdio.h>
#include <unistd.h>

void bubble_sort(int);
void fill();

int a[6];

int main()
{	
	int n = 6;
	int i;

	fill();
	bubble_sort(n);

	for(i=0;i<n;++i)	
		printf(" %d\n",a[i]);
	
	return 0;
}

void fill()
{
	int i;
	srand(getpid());
	
	for(i=0;i<100;++i)
	{
		a[i] = rand()%100;
	}
}


void bubble_sort(int n)
{
	int i,j,temp;
	
	for(i=0;i<n-1;++i)
	{
		for(j=i+1;j<n;++j)	
		{
			if(a[i] < a[j])		
			{
				temp = a[i];
				a[i] = a[j];
				a[j] = temp;			
			}
		}
	}
}


















