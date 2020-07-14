#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <ctime>
#include <numeric>
#include <math.h>
#include <stdio.h>

#include "gaussIntegration.hh"
#include "simpsonsIntegration.hh"
#include "trapezoidIntegration.hh"

using namespace std;

// static const int npts = 2001; // number of points
double intervalNumber = 999; // number of  intervals
double integralStart = 0;    // start of the integration
double integralEnd = 2;      // end of the integration

double f(double x) // function of which the integral is calculated
{
    return exp(x);
}

int main()
{

    double gaussResult = gaussInt(intervalNumber, integralStart, integralEnd);
    double simpsonsResult = simpsonsInt(intervalNumber, integralStart, integralEnd);
    double trapeziodResult = trapezoidInt(intervalNumber, integralStart, integralEnd);

    // output results
    cout << "\n"
         << "gauss: " << gaussResult << "\n"
         << "simpsons: " << simpsonsResult << "\n"
         << "trapeziod: " << trapeziodResult << "\n";

    return 0;
}
