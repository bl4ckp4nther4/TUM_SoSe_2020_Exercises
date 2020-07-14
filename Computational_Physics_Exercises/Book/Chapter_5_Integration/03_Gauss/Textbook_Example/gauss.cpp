// gauss.c : Points and weights for Gaussian quadrature
// comment : this file has to reside in the same directory as integ.c

#include <math.h>

void gauss(int npts, int job, double a, double b,
           double x[], double w[])
{
    // npts number of p oints
    // job= 0 rescaling uniformly between ( a , b )
    // 1 for integral ( 0 , b ) with 50% pts inside ( 0 , ab / ( a+b )
    // 2 for integral ( a , inf ) with 50% inside ( a , b+2a )
    // x , w output grid points and weights .
    int m, i, j;
    double t, t1, pp, p1, p2, p3;
    double pi = 3.1415926535897932385E0;
    double eps = 3.0E-10; // eps = accuracy t o adjus t

    m = (npts + 1) / 2;

    for (i = 1; i <= m; i++)
    {
        t = cos(pi * (i - 0.25) / (npts + 0.5));
        t1 = 1;
        while ((fabs(t - t1)) >= eps)
        {
            p1 = 1.0;
            p2 = 0.0;
            for (j = 1; j <= npts; j++)
            {
                p3 = p2;
                p2 = p1;
                p1 = ((2 * j - 1) * t * p2 - (j - 1) * p3) / j;
            }
            pp = npts * (t * p1 - p2) / (t * t - 1);
            t1 = t;
            t = t1 - p1 / pp;
        }
        x[i - 1] = -t;
        x[npts - i] = t;
        w[i - 1] = 2.0 / ((1 - t * t) * pp * pp);
        w[npts - i] = w[i - 1];
    }
    if (job == 0)
    {
        for (i = 0; i < npts; i++)
        {
            x[i] = x[i] * (b - a) / 2.0 + (b + a) / 2.0;
            w[i] = w[i] * (b - a) / 2.0;
        }
    }
    if (job == 1)
    {
        for (i = 0; i < npts; i++)
        {
            x[i] = a * b * (1 + x[i]) / (b + a - (b - a) * x[i]);
            w[i] = w[i] * 2 * a * b * b / ((b + a - (b - a) * x[i]) * (b + a - (b - a) * x[i]));
        }
    }
    if (job == 2)
    {
        for (i = 0; i < npts; i++)
        {
            x[i] = (b * x[i] + b + a + a) / (1 - x[i]);
            w[i] = w[i] * 2 * (a + b) / ((1 - x[i]) * (1 - x[i]));
        }
    }
}