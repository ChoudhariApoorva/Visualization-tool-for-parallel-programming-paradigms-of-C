#include <stdio.h>

void foo(int x);
void bar(int y);

int main()
{
	int a = 20;
	foo(a);
	return 0;
}

void foo(int x)
{
	int b = 20;
	bar(b);
}

void bar(int y)
{
	int c = 30;
}

