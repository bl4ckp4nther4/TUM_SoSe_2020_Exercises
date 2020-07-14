#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <ctime>
#include <numeric>
#include <math.h>
#include <stdio.h>

using namespace std;

#include "gaussPoints.hh"

double gaussInt(int no, double min, double max)
{
    double f(double x);
    double quadra = 0;

    gaussPoints gaussPoints(no, 0, min, max); // return gauss points and weights

    for (int n = 0; n < no; n++) // calculate integral
    {
        quadra = quadra + f(gaussPoints.x[n]) * gaussPoints.w[n];
    }

    return quadra;
}
