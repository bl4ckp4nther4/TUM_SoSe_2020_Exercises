#include <stdio.h>
#include <math.h>
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>

using namespace std;

// this program will provide an approximation of pi by monte carlo integration by stone throwing

int main()
{
    srand(time(NULL)); // seeding the rand() function with a new seed each time

    int N = 1e8;      //iterations
    int N_int = 1000; // devisions of the interval
    double r;
    double x;                    // random x coordinate between -1 and 1
    double y;                    // random y coordinate between -1 and 1
    double distanceFromCenterSq; // distance from the center
    double N_in = 0;             // number of points in the circle (pond)
    double N_out = 0;            // number of points outside of the circle (pond)
    double areaApprox;

    for (long i = 0; i < N; i++)
    {

        // creating a point inside a -1 to 1 square box
        r = rand() % N_int;
        x = double(r) / double(N_int) * 2 - 1;
        r = rand() % N_int;
        y = double(r) / double(N_int) * 2 - 1;

        //cout << x << "," << y << ",\n";
        //cout << r << "\n";

        // measuring the distance from the center squared
        distanceFromCenterSq = x * x + y * y;

        // if the distance from the center is smaller than one the point is in the circle
        if (distanceFromCenterSq < 1)
        {
            N_in = N_in + 1;
        }
        if (distanceFromCenterSq > 1)
        {
            N_out = N_out + 1;
        }
    }

    areaApprox = N_in / (N_in + N_out) * 4; // Area of the box is 4

    cout << areaApprox;
}