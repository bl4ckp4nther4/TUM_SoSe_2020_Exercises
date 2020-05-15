// this file will compute the integral of f(t) with the gauss method

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
