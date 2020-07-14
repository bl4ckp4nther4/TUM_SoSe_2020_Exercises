#include<stdio.h>
#include<math.h>
#include <stdlib.h>
#include <float.h>

// function declaration
double InDecrease(double under, double over, int N);


int main(){
	// declaration
	double under = 1;
	double previousOver;
	double over = 1;
	int N;
	
// calculation
	
	//for loop increases N
	for (int N=1;N<10^100;N++){
		// calculate the new over
		previousOver = over;
		over = InDecrease( 1, 1, N);
		
		// test if it has reached the upper limit
		if (over == 1.0/0.0) {
			break;
		}
	}
	
	// output values
	printf("previous Over = %500f, \n Over = %500f\n", previousOver, over);
	
}

// function that increases / decreases N times
double InDecrease(double under, double over, int N) { 
	//calculation
	for (int n=1;n<N;n++){
		under = under/2;
		over = over*2;
	}
	
	return over;
	 
}