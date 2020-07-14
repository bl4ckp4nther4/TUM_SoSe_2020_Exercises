#include<stdio.h>
#include<math.h>
#include <iostream>
#include <fstream>

using namespace std;

int main(){

    // declarations
    int L = 25;
    double x = 10;                           // the x of the Bessel function
    double j_0_analytic;                // First term analytically solved, normalization factor for the down sequence
    double j_Up[L+1];                   // Calculated Bessel functions from the recursive up calculation
    double j_Down_C[L+1];               // Calculated Bessel functions from the recursive down calculation#
    double j_Down_Normalized[L+1];      // Normalized Bessel functions from the recursive down calculation
    double relError[L+1];

    printf("Calculate Bessel functions at x = %f\n\n", x);




    // calculating the bessel function upwards
    // ===================================================================================================

    j_Up[0] = sin(x) / x;                       // the first term is neccesary to calculate the next terms 
    j_Up[1] = sin(x) / (x*x) - cos(x) / x ;     // the second term is neccesary to calculate the next terms 

    // calculate the non-normalized values
    for (int l = 1; l <= L; l++) 
    {
        // calculate j_l_plus_1 recursively
        j_Up[l+1] = (2*(double)l + 1) / x * j_Up[l] - j_Up[l-1];  
    }




    // calculating the bessel function downwards
    // ===================================================================================================

    // arbitrary values can be set for the last and second to last terms, as there will be a normalization process
    j_Down_C[L+1] = 1;                       // the last term is neccesary to calculate the previous terms 
    j_Down_C[L] = 1;     // the second to last term is neccesary to calculate the previous terms 
    
    for (int l = L; l >= 1; l--) 
    {
        // calculate j_l_plus_1 recursively
        j_Down_C[l-1] = (2*(double)l + 1) / x * j_Down_C[l] - j_Down_C[l+1];  
    }
    



    // normalizing the calculated down Bessel functions and print out solutions and relative error
    // =========================================================================================================

    // the first term of the up sequence was computed analytically, can be used as normalization factor
    j_0_analytic =  j_Up[0];

    for (int l = 0; l <= L+1; l++)
    {
        // Normalization
        j_Down_Normalized[l] = j_Down_C[l]*j_0_analytic/j_Down_C[0];
    }
    



    // printing out the table with all results and calculating relative error
    //============================================================================================================

    printf("         j_Down               j_Up                 Relative Error\n"); // header for the print out table
    printf("---------------------------------------------------------------------\n");

    for (int l = 0; l <= L+1; l++)
    {
        // relative error
        relError[l] = fabs( j_Up[l] - j_Down_Normalized[l] ) / ( fabs(j_Up[l]) + fabs(j_Down_Normalized[l]));

        // print out
        printf("l = %2i:   %.10e,   %.10e,   %.10e,\n", l, j_Down_Normalized[l], j_Up[l], relError[l]);


    }
}
