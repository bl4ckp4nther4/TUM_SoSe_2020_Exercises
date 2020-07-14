#include<stdio.h>
#include<math.h>

// function declaration
double InDecrease(double under, double over, int N);


int main(){
	// declaration
	double under = 1;
	double previousUnder;
	double over = 1;
	int N;
	
// calculation
	
	//for loop increases N
	for (int N=1;N<10^100;N++){
		// calculate the new under
		previousUnder = under;
		under = InDecrease( 1, 1, N);
		
		// test if it has reched the lower limit
		if (under == 0) {
			break;
		}
	}
	
	// output values
	printf("previous Under =%.500f, \n Under=%.500f\n", previousUnder, under);
	
}

// function that increases / decreases N times
double InDecrease(double under, double over, int N) { 
	//local var declaration
	double under_over[2];
	
	//calculation
	for (int n=1;n<N;n++){
		under = under/2;
		over = over*2;
	}
	under_over[0] = under;
	under_over[1] = over;
	
	return under;
	 
}