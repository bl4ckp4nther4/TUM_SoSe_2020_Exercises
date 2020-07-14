#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <ctime>
#include <numeric>
#include <math.h>
#include <stdio.h>

using namespace std;

// approximating integral with the trapzoid rule for f(t) = t^2

int main()
{
    double min = 0; // integral first endpoint
    double max = 2;
    int no = 100; // number of points (not intervals), needs to be even

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

        sum = sum + w * t; // adding all the values of the function t times the width h
    }

    printf("The integral from %.1f to %.1f of the function f(t) = t^2 with %i points was approximated to %f", min, max, no, sum);
}