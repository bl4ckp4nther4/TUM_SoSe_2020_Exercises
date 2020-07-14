#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <ctime>
#include <numeric>
#include <math.h>
#include <stdio.h>

using namespace std;

double trapezoidInt(int no, double min, double max) // calculate the integral with the trapez rule
{
    double f(double x);
    double sum = 0;                    // sum for summing the different parts together
    double h = (max - min) / (no - 1); // width of deviding integrals
    double t;                          // function variable
    double w;                          // weight of points ( Endpoint are weighted only half )

    for (int n = 1; n <= no; n++)
    {
        t = min + (n - 1) * h;
        if (n == 1 || n == no)
        {
            w = h / 2; // endpoint have only half the weight
        }
        else
        {
            w = h;
        }

        sum = sum + w * f(t); // adding all the values of the function t^2 times the width h
    }
    return sum;
}