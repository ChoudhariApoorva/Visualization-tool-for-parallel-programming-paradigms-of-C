#include <stdio.h>

struct student
{
	int usn;
	double gpa;
};

int main()
{
	struct student S;
	S.usn = 200;
	S.gpa = 9.9;
	
	printf("Usn = %d\tGpa = %f\n",S.usn,S.gpa);
	
	return 0;
}
