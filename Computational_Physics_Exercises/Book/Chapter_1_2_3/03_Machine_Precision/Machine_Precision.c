#include<stdio.h>
#include<math.h>


// function declaration
double Decrease(double Epsilon, int N);



int main(){
	// declaration
	double Epsilon = 1;
	double previousEpsilon;
	double One;
	double previousOne;
	int N;
	
	for (int N=1;N<10^100;N++){
		// calculate the new under
		previousEpsilon = Epsilon;
		previousOne = One;
		
		Epsilon = Decrease( 1, N);
		One = 1 + Epsilon;
		
		// test if it has reched the lower limit
		if (One == 1) {
			break;
		}
	}
	
	// Output
	printf(" previous Epsilon =%.500f, \n previous One =%.500f\n", previousEpsilon, previousOne);
	printf(" Epsilon =%.500f, \n One =%.500f\n", Epsilon, One);
		
	
}


// function that  decreases N times
double Decrease(double Epsilon, int N) { 
	
	//calculation
	for (int n=1;n<N;n++){
		Epsilon = Epsilon/2;
	}
	
	return Epsilon;
	 
}