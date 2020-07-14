#include<stdio.h>
#include<math.h>
#include <iostream>
#include <fstream>


using namespace std;

int main(){
    // declarations
    double termUp;
    double sumUp = 0;
    double termDown;
    double sumDown = 0;
    double Xdata;
    double Ydata;

    // opening the file
    ofstream myfile;
    myfile.open ("sumUpDown.csv");      //opening the files
    

    //going through N 
    for (double N = 1; N <= 100000; N++)
    {
        // Sum up
        for (double n = 1; n <= N; n++)
        {
            termUp = 1/n;
            sumUp = termUp + sumUp;
        }
    
        // Sum down
        for (double n = N; n >= 1; n--)
        {
            termDown = 1/n;
            sumDown = termDown + sumDown;
        }
        // calculating the plot data
        Xdata = log(N)/log(10.0);
        Ydata = (sumUp - sumDown)/(fabs(sumUp) + fabs(sumDown));
        Ydata = log(Ydata)/log(10.0);

        // write data to files
        myfile << Xdata;
        myfile << ",";
        myfile << Ydata;
        myfile << ",";
        myfile << "\n";
    
    }

    myfile.close();         //close the file

    return 0;
}    