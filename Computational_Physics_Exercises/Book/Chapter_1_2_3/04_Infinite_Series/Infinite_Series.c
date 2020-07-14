#include<stdio.h>
#include<math.h>

int main(){
	// declaration
	double epsilon = pow(10, -8);
	double x;
	
	int n;
	double term;
	double sum;
	
	double relError;
	
	// user input: where to calculate x
	x = -500;
	printf("Calculate exp(-x) at x = %f\n", x);

	// summation

	/* initial conditons:
	we start with n=1, which means that sum = 1 and term = 1, for the n=0 term.
	*/
	
	n = 1;						// 
	term = 1;
	sum = 1;
	
	// summing the terms until last term is smaller (relative) than epsilon
	while (fabs(term/sum) > epsilon) {
		
		term = -term * x/n;			// calculate the new term iteratively
		sum = sum + term;			// calculate sum
		
		//printing values in each iteration
		// printf("\n");
		// printf("%i\n", n);
		// printf("%.9f\n", term);
		// printf("%.9f\n", sum);

		n = n+1;						// increase n each iteration
		
	}
	
	relError = fabs(sum - exp(-x))/exp(-x); // relative Error
	
	// output
	printf("x  nmax  sum  |sum - exp(-x)|/exp(-x)\n");
	printf("%f  %i  %f  %f", x, n, sum, relError);
	
}
