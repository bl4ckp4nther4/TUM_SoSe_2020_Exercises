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
	x = 708;
	printf("Calculate exp(-x) at x = %f\n\n", x);

	// summation
	// ===========================================================================

	// we start with n=1, which means that sum = 1 and term = 1, for the n=0 term.
	n = 1;						
	term = 1;
	sum = 1;
	
	// summing the terms until last term is smaller (relative) than epsilon
	while (fabs(term) > epsilon*fabs(sum)) {
		term = term * x/n;			// calculate the new term iteratively
		sum = sum + term;			// calculate sum
		n = n+1;					// increase n each iteration

		// printf("%i, %.6e, %.6e,\n", n, term, 1/sum);
	}
	
	relError = fabs( 1/sum - exp(-x))/exp(-x); // relative Error
	
	// output
	printf("\nx           nmax      sum                 |sum - exp(-x)|/exp(-x)\n");
	printf("%f   %i         %.10e   %.10e", x, n, 1/sum, relError);
	
}
