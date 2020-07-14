#include<stdio.h>
#include<math.h>
#include <iostream>
#include <fstream>

using namespace std;


// function declaration
double calculateSum_1(int N);
double calculateSum_2(int N);
double calculateSum_3(int N);

int main(){
    // declarations
    float epsilon = pow(10, -8);    // smallest error
    float sum_1[100000];    
    float sum_3[100000];

    //calculate the sums 1 and 3 
    for (int N = 1; N <= 100000; N++)
    {               
        sum_1[N-1] = calculateSum_1(N);
        sum_3[N-1] = calculateSum_1(N);
        // printf("\n%f", sum_3[N-1]);
    }



    // writing the sum 1 and sum 2 data into file 
    ofstream myfile;
    myfile.open ("Sum1_Sum3.txt");
    myfile << sum_1;
    myfile.close();

    return 0;

}

double calculateSum_1(int N) // calculate the first sum until N
{
    // summation 1:
    float n_1 = 1;  // the summation starts at n_1 = 1
    float term_1;                   // term for the first summation
    float sum_1 = 0;                // term for the first summation     
    
    while (n_1 < N) {

        term_1 = pow(-1, n_1)*n_1/(n_1+1);  //the nth term

        sum_1 = sum_1 + term_1;       //the sum at the nth 
        
        //printing values in each iteration
		// printf("\n");
		// printf("%i\n", n_1);
		// printf("%.9f\n", term_1);
		// printf("%.9f\n", sum_1);

        n_1++; // increasing n_1 with each iteration

        
    }
    return sum_1;
}

double calculateSum_2(int N) // calculate the second sum until N
{
    // local variable declaration
    float term_2_1;                 // first term for the second summation
    float term_2_2;                 // second term for the second summation
    float sum_2_1 = 0;              // first sum for the second summation
    float sum_2_2 = 0;              // second sum for the second summation
    float sum_2 = 0;                // final sum for the second summation   

    float n_2 = 1;  // the summation starts at n_2 = 1

    while (n_2 < N) {

        term_2_1 = ( 2*n_2 - 1 )/ (2 * n_2);
        term_2_2 = ( 2*n_2 ) / ( 2*n_2 + 1 );  

        sum_2_1 = sum_2_1 + term_2_1;
        sum_2_2 = sum_2_2 + term_2_2; 

        //printing values in each iteration
		// printf("\n");
		// printf("%f\n", n_2);
		// printf("%f\n", term_2_1);
		// printf("%f\n", term_2_2);

        n_2++; // increasing n_2 with each iteration
    }
    // final summation of the seperate sums
    sum_2 = - sum_2_1 + sum_2_2;


    // output
	// printf("\nnmax_2     sum_2      term_2_1   term_2_1\n");
	// printf("%.1f  %.7f  %.7f  %.7f\n", n_2, sum_2, term_2_1, term_2_2);

    return sum_2;
}

double calculateSum_3(int N) // calculate the third sum until N
{
    //local variable declaration
    float term_3;                   // term for the third summation
    float sum_3 = 0;                // sum for the third summation
    float n_3 = 1;  // the summation starts at n_1 = 1

    while (n_3 < N) {

        term_3 = 1/( 2*n_3 * ( 2*n_3 + 1 ) );  //the nth term

        sum_3 = sum_3 + term_3;       //the sum at the nth 
        
        //printing values in each iteration
		// printf("\n");
		// printf("%i\n", n_1);
		// printf("%.9f\n", term_1);
		// printf("%.9f\n", sum_1);

        n_3++; // increasing n_1 with each iteration

        
    }
    
    // output
	// printf("\nnmax_3     sum_3       term_3\n");
	// printf("%.1f  %.7f  %.7f\n", n_3, sum_3, term_3);

    return sum_3;
}