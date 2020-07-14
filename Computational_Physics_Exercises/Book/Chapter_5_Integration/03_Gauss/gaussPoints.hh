#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <ctime>
#include <numeric>
#include <math.h>
#include <stdio.h>

using namespace std;

static const double ME = 2.7182818284590452354; // eulers constant
static const double pi = 3.14159265359;

double eps = 3e-14; // adjust accuracy

class gaussPoints
{
public:
    int m = 0;

    double t = 0;
    double t1 = 0;

    double pp = 0;
    double p1 = 0;
    double p2 = 0;
    double p3 = 0;
    double xi;

    int job;
    double a;
    double b;

    double *x; // gausspoint x
    double *w; // gausspoint weight

    gaussPoints(int npts, int job, double a, double b)
    {
        this->job = job;
        this->a = a;
        this->b = b;

        w = new double[npts];
        x = new double[npts];

        m = (npts + 1) / 2;
        for (int i = 1; i <= m; i++)
        {
            t = cos(pi * ((double)i - 0.25) / (npts + 0.5));
            t1 = 1;
            while (fabs(t - t1) >= eps)
            {
                p1 = 1;
                p2 = 0;
                for (int j = 1; j <= npts; j++)
                {
                    p3 = p2;
                    p2 = p1;
                    p1 = ((2.0 * (double)j - 1.0) * t * p2 - ((double)j - 1.0) * p3) / ((double)j);
                }
                pp = npts * (t * p1 - p2) / (t * t - 1.0);
                t1 = t;
                t = t1 - p1 / pp;
            }
            x[i - 1] = -t;
            x[npts - i] = t;
            w[i - 1] = 2.0 / ((1.0 - t * t) * pp * pp);
            w[npts - i] = w[i - 1];
            //printf("x[i-1] = %f, w = %f ", x[i - 1], w[npts - i]);
        }
        //printf("\n");

        if (job == 0)
        {
            for (int i = 0; i < npts; i++)
            {
                x[i] = x[i] * (b - a) / 2 + (b + a) / 2;
                w[i] = w[i] * (b - a) / 2;
            }
        }

        if (job == 1)
        {
            for (int i = 0; i < npts; i++)
            {
                xi = x[i];
                x[i] = a * b * (1 + xi) / (b + a - (b - a) * xi);
                w[i] = w[i] * 2 * a * b * b / ((b + a - (b - a) * xi) * (b + a - (b - a) * xi));
            }
        }
        if (job == 2)
        {
            for (int i = 0; i < npts; i++)
            {
                xi = x[i];
                x[i] = (b * xi + b + a + a) / (1 - xi);
                w[i] = w[i] * 2 * (a + b) / ((1 - xi) * (1 - xi));
            }
        }
        /*
    */
    }

    ~gaussPoints()
    {
        cout << "The class gaussPoints has been destroyed.\n";
    }
};