#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <ctime>
#include <numeric>
#include <math.h>
#include <stdio.h>

using namespace std;

// approximating integral with the Simpsons rule for f(t) = sin(t)

int main()
{
    double A = 0; // integral first endpoint
    double B = 1;
    int N = 2001; // number of points (not intervals), needs to be odd

    double sum = 0;                // sum for summing the different parts together
    double h = (B - A) / (N - 1);  // width of deviding integrals
    double t;                      // function variable
    double w;                      // weight of points ( Endpoint are weighted only half )
    double w_sum = 0;              // testsum of the weights
    double epsilon = pow(10, -10); // maximum deviation of the test sum, from expected value

    for (int n = 1; n <= N; n++)
    {

        t = A + ((double)n - 1) * h; // value of variable in iteration

        if (n % 2 == 0)
        {
            w = 4 * h / 3; // even n weight
        }
        if (n % 2 == 1 && n != 1 && n != N)
        {
            w = 2 * h / 3; // odd weight n (without endpoints)
        }
        if (n == 1 || n == N)
        {
            w = h / 3; // endpoint weight
        }
        w_sum = w_sum + w;

        sum = sum + w * t; // adding all the values of the function t^2 times the width h
    }

    if (w_sum <= (N - 1) * h + epsilon && w_sum >= (N - 1) * h - epsilon) // checking the sum of the weights
    {
        printf("The integral from %.1f to %.1f of the function f(t) = sin(t() with %i points was approximated to %f", A, B, N, sum);
    }
    else
    {
        printf("ERROR: Sum of weights has unexpected value: %.10f, expected value: %.10f", w_sum, (N - 1) * h);
    }
}