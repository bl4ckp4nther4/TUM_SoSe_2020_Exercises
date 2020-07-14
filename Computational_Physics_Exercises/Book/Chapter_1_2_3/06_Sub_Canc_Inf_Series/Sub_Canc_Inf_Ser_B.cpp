#include<stdio.h>
#include<math.h>
#include <iostream>
#include <fstream>

using namespace std;

int main(){
    // declarations
    int N = 1000000;
    double sum_1[2];    
    double sum_3[2];
    double term_1;                   // term for the first summation
    double term_3;                   // term for the third summation
    
    double Xdata;
    double Ydata;
    
    // opening the file
    ofstream myfile;
    myfile.open ("Sum1_Sum3.csv");      //opening the file

    //calculate the sums 1 and 3 
    sum_1[0] = 0;                           // initial state for the sum is zero
    sum_3[0] = 0;                           // initial state for the sum is zero

    for (double n = 1; n <= N; n++)
    {
        //calculate the sums
        term_1 = pow(-1, n)* n /( n +1);        // the nth term
        sum_1[1] = sum_1[0] + term_1;     // the sum at the nth 
        
        term_3 = 1/( 2* n * ( 2* n +1 ) );   // the nth term
        sum_3[1] = sum_3[0] + term_3;     // the sum at the nth 

        //calculate the data for the log-log-plot
        Xdata = log(n)/log(10);
        Ydata = log(fabs( ( sum_1[1] - sum_3[1] )/sum_3[1] ));

        //write every 100th datapoint to file
        if((int)n % 100 == 0)
        {
            myfile << Xdata;
            myfile << ",";
            myfile << Ydata;
            myfile << ",";
            myfile << "\n";
        }

        // set the n-1 sums to n
        sum_1[0] = sum_1[1];
        sum_3[0] = sum_3[1];
        
    }


    myfile.close();         //close the file

    return 0;

}

